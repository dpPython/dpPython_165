import json
import os
from datetime import datetime as dt

DIR = os.path.abspath(os.path.dirname(__file__))

CURRENCY = {
    '₴': 'UAH',
    '$': 'USD',
    '€': 'EUR'
    }


def process_currency(value):
    separetaor = len(value) - 1
    currency_value = value[:separetaor]
    currency = CURRENCY.get(value[separetaor:])
    return [currency, currency_value]


def process_publish_date(value):
    today = dt.today()
    publish = dt.strptime(value, "%m/%d/%Y")
    return False if today < publish else False



ACTIONS = {
    'get_currency': process_currency,
    'due_to': process_publish_date,
    '': lambda x: x
    }


class FileParser:
    def __init__(self, parser_name):
        self.parser_name = parser_name

    @property
    def parser(self):
        with open(os.path.join(DIR, "{parser_name}.json".format(
                parser_name=self.parser_name)), 'r') as par:
            return json.load(par)
