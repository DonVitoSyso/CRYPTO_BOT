import json
import requests
from utils import key_API, values

class APIException(Exception):
    pass

class ValuesConvert():
    @staticmethod
    def get_price(vals: dict):
        # Обрабатываем исключения
        if len(vals) != 3:
            raise APIException(f'Неверный запрос. Вводить запрос в одну строку через пробел - 3 параметра')

        base, quote, amount = vals

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amnt}. Количество ввалют должно быть введенно цифрой')

        try:
            bs_ = values[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {qt_}.')

        try:
            qt_ = values[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {bs_}.')

        if qt_ == bs_:
            raise APIException(f'Валюта {bs_} не может быть переведена в валюту {qt_} - одинаковые!')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={bs_}{qt_}&key={key_API}')
        # content = {'status': 200, 'message': 'rates', 'data': {'USDRUB': '64.1824'}}
        txt_API_json = json.loads(r.content)['data'][f'{bs_}{qt_}']
        text = f'Цена {amount} {bs_} в {qt_} - {float(txt_API_json)*amount}'
        return text
