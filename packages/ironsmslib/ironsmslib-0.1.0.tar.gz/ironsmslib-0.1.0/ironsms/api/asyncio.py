from typing import List, Optional, Literal, Union

import httpx
from ..exceptions import errors
from ..types import Country, Balance, Phone


class AsyncIronSMS:
    base_api_url: str = 'http://iron-sms.com/api/v1/'
    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = httpx.AsyncClient()

    def __process_errors(self, response: dict):
        for exc in errors:
            if exc.message in str(response):
                raise exc(response)

    async def _request(self, method: str, params: Optional[dict] = None):
        if params is None:
            params = {}

        params['api_key'] = self.api_key
        res = await self.session.get(self.base_api_url + method, params=params)
        response = res.json()
        if response['status'] == 'fail':
            self.__process_errors(response)
        return response

    async def get_countries(self) -> List[str]:
        response = await self._request('getCountries')
        return response['data']

    async def get_services(self):
        response = await self._request('getServices')
        return response['data']

    async def get_prices(self, country: str = 'US') -> Country:
        response = await self._request('getPrices', params={'country': country})
        result = Country(**response['data'])
        return result

    async def get_balance(self) -> Balance:
        response = await self._request('getBalance')
        result = Balance(**response['data'])
        return result

    async def get_number(self, country: str, service: str) -> Phone:
        response = await self._request('getNumber', params={
            'country': country,
            'service': service
        })
        result = Phone(**response['data'])
        return result

    async def set_status(self, status: int, id: int) -> Literal[True]:
        response = await self._request('setStatus', params={
            'status': status,
            'id': id
        })
        return True

    async def get_status(self, id: int) -> Union[Literal[False], int]:
        response = await self._request('getStatus', params={
            'id': id
        })

        if response['status'] == 'wait':
            return False
        elif response['status'] == 'success':
            return response['code']
