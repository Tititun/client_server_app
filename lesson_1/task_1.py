# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в
# строковом формате и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в
# формат Unicode и также проверить тип и содержимое переменных.

# для отправки запроса на сайт исользовал библиотеку requests:
# pip3 install requests

import requests
import json


def check_type_and_content(text):
    """функция для вывода типа и содержимого переменной"""
    print(f'{type(text)}: {text}')


def to_unicode_escape(text):
    """функция для получения unicode_escape вводимого текста с сайта
     dencode.com"""
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0)'
                      ' Gecko/20100101 Firefox/96.0'}
    data = {"type": "string",
            "method": "string.unicode-escape",
            "value": text,
            "oe": "UTF-8",
            "options": {"encStrUnicodeEscapeSurrogatePairFormat": ""}
            }
    try:
        response = requests.post('https://dencode.com/dencode', headers=headers,
                             data=json.dumps(data))
        return response.json()['response']['encStrUnicodeEscape']
    except (requests.RequestException, ValueError):
        return 'server error'


if __name__ == '__main__':
    for word in ['разработка', 'сокет', 'декоратор']:
        check_type_and_content(word)
        unicode_escape = to_unicode_escape(word)
        if unicode_escape != 'server error':
            check_type_and_content(unicode_escape)
        else:
            print(unicode_escape)
        print('------------------')
