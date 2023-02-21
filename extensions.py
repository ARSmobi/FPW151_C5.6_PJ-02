import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Две одинаковые валюты не конвертируются.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не доступна.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюта {base} не доступна.')

        try:
            amount = float(amount)
        except ValueError:
            APIException('Неверно записано количество валюты.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
