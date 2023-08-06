# Iron Sms Library
Library for API [iron-sms.com](https://iron-sms.com)

#Features:  
     [+] Full support API from 14.08.2021   
     [+] Support for both sync and async

#Example
A small synchronous example
```
from ironsms import SyncIronSMS
from loguru import logger

from ironsms.exceptions import BadQueryException

api = SyncIronSMS('YOUR_API_KEY')

balance = api.get_balance()
logger.info(f'Your balance: {balance.balance}')

services = api.get_services()
logger.info(f'All services: {services}')

countries = api.get_countries()
logger.info(f'All countries: {countries}')

prices = api.get_prices('US')
logger.info(f'USA prices: {prices}')
```

#Install
`pip install ironsmslib`
