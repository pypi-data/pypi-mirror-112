import requests
import hashlib
import base64
import time
import hmac

from requests.adapters import HTTPAdapter
from urllib.parse import urlparse


class HTTPtimeoutAdapter(HTTPAdapter):
    """ Adds timeout to requests HTTP adapter """

    def __init__(self, timeout: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = timeout

    def send(self, *args, **kwargs):
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout
        return super(HTTPtimeoutAdapter, self).send(*args, **kwargs)


class LMBase(requests.Session):
    _DEVICES_ROOT = 'device/devices'

    _HEADERS = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization': None,
        'X-version': '2'
    }

    def __init__(self, account_name: str, access_id: str, api_key: str, global_timeout: int = 5):
        """
        API to logic monitor
        :param account_name: Logic monitor account name
        :param access_id: Logic monitor API access ID
        :param api_key: API key
        :param global_timeout: Request timeout in seconds for every request within the session
        """

        super().__init__()
        self.account_name = account_name
        self.access_id = access_id
        self._api_key = api_key

        self._devices_base_url = f'https://{self.account_name}.logicmonitor.com/santaba/rest/{self._DEVICES_ROOT}'

        self._adapter = HTTPtimeoutAdapter(global_timeout)
        self.mount('http://', self._adapter)
        self.mount('https://', self._adapter)

        self.headers.update(self._HEADERS)

    def __repr__(self):
        return f'{self.__class__.__name__}(account_name="{self.account_name}, access_id={self.access_id}")'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def close_session(self):
        """ Closes requests session """

        self.close()

    def _construct_auth_header(self, http_method: str, url: str, data: str):
        """ Constructs the LM authorization header """

        # Get current time in milliseconds
        epoch = str(int(time.time() * 1000))

        # Concatenate Request details
        resource_path = urlparse(url).path.replace('/santaba/rest', '')
        request_vars = http_method.upper() + epoch + data + resource_path

        # Construct signature
        h = hmac.new(
                key=bytes(self._api_key.encode()),
                msg=bytes(request_vars.encode()),
                digestmod=hashlib.sha256
            )
        s: bytes = base64.b64encode(bytes(h.hexdigest().encode()))
        signature = s.decode()

        # Construct headers
        self.headers.update(
            {
                'Authorization': f'LMv1 {self.access_id}:{signature}:{epoch}'
            }
        )

    def get(self, url: str, **kwargs) -> requests.Response:
        """ HTTP GET request. Creates the authorization headers """

        self._construct_auth_header('GET', url, '')
        return super(LMBase, self).get(url, **kwargs)
