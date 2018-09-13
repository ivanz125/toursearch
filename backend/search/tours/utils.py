import datetime
import requests


def country_name(code):
    if code == 'bg':
        return 'Болгария'
    elif code == 'gr':
        return 'Греция'
    elif code == 'ge':
        return 'Грузия'
    elif code == 'do':
        return 'Доминикана'
    elif code == 'eg':
        return 'Египет'
    elif code == 'il':
        return 'Израиль'
    elif code == 'id': # Indonesia
        return 'Индонезия'
    elif code == 'es':
        return 'Испания'
    elif code == 'it':
        return 'Италия'
    elif code == 'cy':
        return 'Кипр'
    elif code == 'cn': # China
        return 'Китай'
    elif code == 'cu': # Cuba
        return 'Куба'
    elif code == 'lv':
        return 'Латвия'
    elif code == 'lt':
        return 'Литва'
    elif code == 'mu': # Mauritius
        return 'Маврикий'
    elif code == 'mv': # Maldives
        return 'Мальдивы'
    elif code == 'mx':
        return 'Мексика'
    elif code == 'ae':
        return 'ОАЭ'
    elif code == 'pt':
        return 'Португалия'
    elif code == 'sc': # Seychelles
        return 'Сейшелы'
    elif code == 'th': # Thailand
        return 'Таиланд'
    elif code == 'tr':
        return 'Турция'
    elif code == 'fr':
        return 'Франция'
    elif code == 'lk': # Sri Lanka
        return 'Шри Ланка'
    elif code == 'ee':
        return 'Эстония'
    return 'Неизвестная страна'


def date_int_to_datetime(date):
    day = date % 100
    date //= 100
    month = date % 100
    date //= 100
    return datetime.date(date, month, day)


def uah_to_eur_rate(db):
    rate = db.currencies.find_one({'pair': 'uah_eur'})
    value = int()
    if rate is None or datetime.datetime.now().timestamp() - rate['time'] > 1600:
        resp = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=UAH_EUR&compact=ultra')
        value = resp.json()['UAH_EUR']
        db.currencies.delete_one({'pair': 'uah_eur'})
        obj = {
            'pair': 'uah_eur',
            'rate': value,
            'time': datetime.datetime.now().timestamp()
        }
        db.currencies.insert_one(obj)
        print("UAH/EUR updated:", value)
    else:
        value = rate['rate']
    return value
