# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате
# JSON с информацией о заказах. Написать скрипт, автоматизирующий его
# заполнение данными.

import json
import random
import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    """
    функция записывает поданные данные в файл 'orders.json'
    """
    out_file = 'orders.json'
    with open(out_file, encoding='utf-8') as f:
        content = json.load(f)

    content['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4)


if __name__ == '__main__':
    for i in range(1, 11):
        write_order_to_json(f'item_{i}',
                            random.randint(1, 10),
                            random.randint(20, 1000),
                            f'client_{i}',
                            str(datetime.date(2021,
                                              random.randint(1, 12),
                                              random.randint(1, 28)))
                            )
