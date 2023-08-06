import httpx
import respx

from . import utils
import xmltodict


class OnlineAfsprakenMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class OnlineAfsprakenAPI(metaclass=OnlineAfsprakenMeta):

    BASE_URL = "https://agenda.onlineafspraken.nl/APIREST"
    params = {}

    def __init__(self):
        # if is_test:
        #     self._setup_test_api(self)
        self._setup_api()

    def _setup_api(self):
        self.client = httpx.Client(base_url=self.BASE_URL)

    def set_params(self, method, **kwargs):
        self.params = utils.build_param(method, **kwargs)

    def get_params(self):
        return self.params

    def get(self, method, **kwargs):
        filter_kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.set_params(method, **filter_kwargs)
        return self.client.get(url="", params=self.params)

    def get_base_url(self):
        return self.BASE_URL
