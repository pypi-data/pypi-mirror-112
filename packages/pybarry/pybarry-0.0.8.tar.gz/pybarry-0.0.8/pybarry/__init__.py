import logging
from datetime import datetime, timedelta

import requests

DEMO_TOKEN = ''
DEFAULT_TIMEOUT = 15

_LOGGER = logging.getLogger(__name__)


class InvalidToken(BaseException):
    pass


class Barry:

    def __init__(
            self,
            access_token=DEMO_TOKEN,
            timeout=DEFAULT_TIMEOUT,
    ):
        self.access_token = access_token
        self.timeout = timeout

    @staticmethod
    def hour_rounder(t):
        # Rounds to nearest hour by adding a timedelta hour if minute >= 30
        return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
                + timedelta(hours=t.minute // 30))

    @staticmethod
    def get_currency(data):
        if data.get('country') == 'DK' or data.get('currency') == 'DKK':
            currency = 'kr./KWH'
        else:
            currency = '€/KWH'
        return currency

    def update_co2_emission(self, price_code):
        current_time = self.hour_rounder(datetime.utcnow().replace(microsecond=0)).isoformat() + 'Z'
        last_hour_date_time = self.hour_rounder(
            (datetime.utcnow() - timedelta(hours=1)).replace(microsecond=0)).isoformat() + 'Z'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }
        price_code = price_code.split('_')[-1]
        data = '{ "jsonrpc": "2.0", "id": 0, "method": "co.getbarry.api.v1.OpenApiController.getHourlyCo2Intensity", "params": [ "%s", "%s", "%s" ] }' % (
            price_code, last_hour_date_time, current_time)
        response = requests.post('https://jsonrpc.barry.energy/json-rpc', headers=headers, data=data)
        json_res = response.json()
        result = json_res.get('result')
        if result:
            result = result[0]
            value = result['carbonIntensity']
            return value, 'gCO2/kWh'
        else:
            return 'NA', '-'

    def update_spot_price(self, price_code):
        current_time = self.hour_rounder(datetime.utcnow().replace(microsecond=0)).isoformat() + 'Z'
        last_hour_date_time = self.hour_rounder(
            (datetime.utcnow() - timedelta(hours=1)).replace(microsecond=0)).isoformat() + 'Z'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }
        data = '{ "jsonrpc": "2.0", "id": 0, "method": "co.getbarry.api.v1.OpenApiController.getPrice", "params": [ "%s", "%s", "%s" ] }' % (
            price_code, last_hour_date_time, current_time)
        response = requests.post('https://jsonrpc.barry.energy/json-rpc', headers=headers, data=data)
        json_res = response.json()
        result = json_res.get('result')
        if result:
            result = result[0]
            value, currency = result['value'], self.get_currency(result)
            return value, currency

    def update_total_price(self, mpid):
        current_time = self.hour_rounder(datetime.utcnow().replace(microsecond=0)).isoformat() + 'Z'
        last_hour_date_time = self.hour_rounder(
            (datetime.utcnow() - timedelta(hours=1)).replace(microsecond=0)).isoformat() + 'Z'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }
        data = '{ "jsonrpc": "2.0", "id": 0, "method": "co.getbarry.api.v1.OpenApiController.getTotalKwHPrice", "params": [ "%s", "%s", "%s" ] }' % (
            mpid, last_hour_date_time, current_time)
        response = requests.post('https://jsonrpc.barry.energy/json-rpc', headers=headers, data=data)
        json_res = response.json()
        result = json_res.get('result')
        if result:
            value, currency = result['value'], self.get_currency(result)
            return value, currency

    def get_all_metering_points(self, check_token=False):
        headers = {
            'Authorization': f'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }

        data = '{ "jsonrpc": "2.0", "id": 0, "method": "co.getbarry.api.v1.OpenApiController.getMeteringPoints", "params": [] }'
        response = requests.post('https://jsonrpc.barry.energy/json-rpc', headers=headers, data=data)
        json_res = response.json()
        if json_res.get('result'):
            if check_token:
                return True
            result = json_res['result']
            res = [(', '.join((data['address']['formattedAddress'], data['mpid'])), data['priceCode']) for data in
                   result]
            return res
        else:
            raise InvalidToken('Invalid access token')
