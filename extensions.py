import json
import requests
from utils import key_API, values

class APIException(Exception):
    pass

class ValuesConvert():
    @staticmethod
    def get_price(vals: dict):
        base, quote, amount = vals

        # Обрабатываем исключения
        if len(vals) != 3:
            raise APIException(f'Неверный запрос. Вводить запрос в одну строку через пробел - 3 параметра')

        try:
            amnt = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amnt}. Количество ввалют должно быть введенно цифрой')

        try:
            qt_ = values[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {qt_}.')

        try:
            bs_ = values[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {bs_}.')

        if base == quote:
            raise APIException(f'Валюта {base} не может быть переведена в валюту {quote} - одинаковые!')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={values[base]}{values[quote]}&key={key_API}')
        # content = {'status': 200, 'message': 'rates', 'data': {'USDRUB': '64.1824'}}
        txt_API_json = json.loads(r.content)['data'][f'{values[base]}{values[quote]}']

        return base, quote, amount, txt_API_json
