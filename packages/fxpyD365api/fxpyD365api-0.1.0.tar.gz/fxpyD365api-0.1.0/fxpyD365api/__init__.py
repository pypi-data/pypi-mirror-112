import os
import json
import adal
import requests
import dateutil
import datetime

__all__ = [
    'GenericWrapper'
]


class D365ApiError(Exception):
    pass


class D36pApiWrapperError(Exception):
    pass


class BaseApiWrapper:
    def __init__(self, crmorg=None, token=None, tenant=None, client_id=None,
                 client_secret=None, api_url='/api/data/v9.0/', extra_headers=None, page_size=100):
        self.crmorg = crmorg or self.get_crmorg()
        self.tenant = tenant
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = token or self._get_token(self.tenant, self.client_id, self.client_secret)
        self.page_size = page_size
        self.current_page = None
        self.page_urls = {}
        self._api_url = api_url
        if extra_headers:
            self.__headers.update(extra_headers)

    entity_type = None

    __headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    @staticmethod
    def get_crmorg():
        org = os.environ.get('D365_ORG_URL', None)
        if org is None:
            raise ValueError(
                '"D365_ORG_URL" must be set as environment variable in case it is not passed as a parameter'
            )
        return org

    def _get_token(self, tenant, client_id, client_secret):
        if tenant is None:
            tenant = os.environ.get('D365_TENANT', None)
        if client_id is None:
            client_id = os.environ.get('D365_CLIENT_ID', None)
        if client_secret is None:
            client_secret = os.environ.get('D365_CLIENT_SECRET', None)
        if not all([tenant, client_id, client_secret]):
            raise ValueError(
                '"D365_TENANT", "D365_CLIENT_ID" and "D365_CLIENT_SECRET" must be set as '
                'environment variable in case they are not passed as a parameters'
            )
        context = adal.AuthenticationContext(f'https://login.microsoftonline.com/{tenant}')
        token = context.acquire_token_with_client_credentials(self.crmorg, client_id, client_secret)
        self.token_expires_at = dateutil.parser.parse(token['expiresOn'])
        return token

    @property
    def token(self):
        if datetime.datetime.now() + datetime.timedelta(minutes=5) > self.token_expires_at:
            self._token = self._get_token(self.tenant, self.client_id, self.client_secret)
        return self._token.get('accessToken')

    @property
    def headers(self):
        headers = self.__headers
        headers.update({'Authorization': f'Bearer {self.token}'})
        return headers

    @property
    def _base_api_url(self):
        return f"{self.crmorg}{self._api_url}"

    @property
    def has_next_page(self):
        return self.current_page and self.page_urls.get(self.current_page + 1) \
               and self.page_urls.get(self.current_page + 1) != '__none__'

    @property
    def api_url(self):
        if not self.entity_type:
            raise NotImplementedError('"entity_type" attribute must be defined in subclasses of BaseApiWrapper')
        return f"{self._base_api_url}{self.entity_type}"

    def _update_prefer_header(self, headers_dict, key, value):
        p_header = headers_dict.setdefault('Prefer', '')
        if p_header:
            hdrs = {}
            for s in p_header.split(','):
                k, v = s.split('=')
                hdrs[k] = v
            hdrs[key] = value
            headers_dict.update(
                {'Prefer': ','.join(['='.join(i) for i in hdrs.items()])}
            )
            return headers_dict
        headers_dict.update(
            {'Prefer': '='.join([key, value])}
        )
        return headers_dict

    def get_page(self, page: int = 1, select=None, request_filter=None, order_by=None, annotations=None):
        """
        Used for getting a first page of list API data,
        or a specific page if such page url has been cached.

        :raises D365ApiError: if http request is not "Ok"
        :raises D36pApiWrapperError: if requested page url is not cached or is out of range
        :param page:
        :param select: string with comma separated attribute names of an entity to include, defaults to all
        :param request_filter: filter string
        :param order_by:
        :param annotations: if set to "*", will include all annotations for related objects
        :return:
        """
        headers = self.headers.copy()
        headers.update(
            {'Prefer': f'odata.maxpagesize={self.page_size}'}
        )
        if annotations:
            headers = self._update_prefer_header(headers, 'odata.include-annotations', f'"{annotations}"')
        params = {}
        if page == 1:
            url = self.api_url
            if select:
                params['$select'] = select
            if request_filter:
                params['$filter'] = request_filter
            if order_by:
                params['$orderby'] = order_by
        else:
            if self.page_urls.get(page) == '__none__':
                raise D36pApiWrapperError(f'The page you requested is out of range.')
            if page not in self.page_urls:
                pages = sorted(self.page_urls.keys())
                raise D36pApiWrapperError(f'The url for the page you requested is not cashed. Available pages are '
                                          f'{pages[0]} trough {pages[-1]}. Try to get the highest available page and'
                                          f' then use "get_next_page()" method until you get to desired page.')
            url = self.page_urls.get(page, None)

        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            self.current_page = page
            self.page_urls[page + 1] = response.json().get('@odata.nextLink', '__none__')
            return response.json()
        else:
            raise D365ApiError({'response_status_code': response.status_code, 'response_data': response.json()})

    def get_next_page(self):
        if self.current_page:
            return self.get_page(page=self.current_page + 1)
        raise D36pApiWrapperError('To call "get_next_page()" "current_page" attribute can not be None. '
                                  'Please call "get_page()" method first.')

    def get_previous_page(self):
        if not self.current_page or self.current_page == 1:
            raise D36pApiWrapperError('To call "get_next_page()" "current_page" attribute can not be None or 1. Please '
                                      'call "get_page()" method or make sure the current page is not first.')
        return self.get_page(page=self.current_page + 1)

    def get_top(self, qty: int, select=None, request_filter=None, order_by=None, annotations=None):
        """
        :raises D365ApiError: if http request is not "Ok"
        :param qty: the number of matching results to return
        :param select:
        :param request_filter:
        :param order_by:
        :param annotations: if set to "*", will include all annotations for related objects
        :return:
        """
        params = {'$top': qty}
        if select:
            params['$select'] = select
        if request_filter:
            params['$filter'] = request_filter
        if order_by:
            params['$orderby'] = order_by
        headers = self.headers.copy()
        if annotations:
            headers = self._update_prefer_header(headers, 'odata.include-annotations', f'"{annotations}"')
        response = requests.get(self.api_url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise D365ApiError({'response_satatus_code': response.status_code, 'response_data': response.content})

    def create(self, data, annotations=None):
        """
        Create entity
        :param data: python dictionary with body content
        :param annotations: string, e.g. "*", will include all annotations for related objects
        :return: response object
        """
        headers = self.headers.copy()
        headers.update({'Prefer': 'return=representation'})
        if annotations:
            headers = self._update_prefer_header(headers, 'odata.include-annotations', f'"{annotations}"')
        return requests.post(self.api_url, headers=headers, json=json.dumps(data))

    def retrieve(self, entity_id, select=None, annotations=None):
        params = {}
        if select:
            params['$select'] = select
        headers = self.headers.copy()
        if annotations:
            headers = self._update_prefer_header(headers, 'odata.include-annotations', f'"{annotations}"')
        return requests.get(f'{self.api_url}({entity_id})', params=params, headers=headers)

    def update(self, entity_id, data, select=None):
        headers = self.headers.copy()
        headers = self._update_prefer_header(headers, 'return', 'representation')
        url = f'{self.api_url}({entity_id})'
        params = {}
        if select:
            params['$select'] = select
        return requests.patch(url, params=params, headers=headers, json=json.dumps(data))

    def delete(self, entity_id):
        return requests.delete(f'{self.api_url}({entity_id})', headers=self.headers)


class GenericWrapper(BaseApiWrapper):
    def __init__(self, entity_type, *args, **kwargs):
        super(GenericWrapper, self).__init__(*args, **kwargs)
        self.entity_type = entity_type
