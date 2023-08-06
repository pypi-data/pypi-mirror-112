from typing import List, Optional, Literal, Union

import httpx
from ..exceptions import errors
from ..types import Country, Balance, Phone


class SyncIronSMS:
    base_api_url: str = 'http://iron-sms.com/api/v1/'
    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = httpx.Client()

    def __process_errors(self, response: dict):
        for exc in errors:
            if exc.message in str(response):
                raise exc(response)

    def _request(self, method: str, params: Optional[dict] = None):
        if params is None:
            params = {}

        params['api_key'] = self.api_key
        res = self.session.get(self.base_api_url + method, params=params)
        response = res.json()
        if response['status'] == 'fail':
            self.__process_errors(response)
        return response

    def get_countries(self) -> List[str]:
        response = self._request('getCountries')
        return response['data']

    def get_services(self) -> List[str]:
        response = self._request('getServices')
        return response['data']

    def get_prices(self, country: str = 'US') -> Country:
        response = self._request('getPrices', params={'country': country})
        result = Country(**response['data'])
        return result

    def get_balance(self) -> Balance:
        response = self._request('getBalance')
        result = Balance(**response['data'])
        return result

    def get_number(self, country: str, service: str) -> Phone:
        response = self._request('getNumber', params={
            'country': country,
            'service': service
        })
        result = Phone(phone=response['phone'], activation_id=response['id'])
        return result

    def set_status(self, status: int, id: int) -> Literal[True]:
        response = self._request('setStatus', params={
            'status': status,
            'id': id
        })
        return True

    def get_status(self, id: int) -> Union[Literal[False], int]:
        response = self._request('getStatus', params={
            'id': id
        })

        if response['status'] == 'wait':
            return False
        elif response['status'] == 'success':
            return response['code']
