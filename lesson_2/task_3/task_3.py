# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт,
# автоматизирующий сохранение данных в файле YAML-формата.

import yaml
import random

rus_words = ['опята', 'ёлка', 'мы', 'береза', 'дорога']

data = [{'my_list': [random.choice(rus_words), random.randint(1, 100)],
         'my_int': random.randint(1, 100),
         'my_dict': {'entry_1': f'{random.randint(1, 100)}'
                                f'{chr(random.randint(256, 1000))}',
                     'entry_2': f'{random.randint(1, 100)}'
                                f'{chr(random.randint(256, 1000))}'}
         } for _ in range(5)]


if __name__ == '__main__':
    file_name = 'task_3.yaml'
    with open(file_name, 'w', encoding='utf-8') as f_n:
        yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True)

    with open(file_name, encoding='utf-8') as f_n:
        loaded = yaml.load(f_n, Loader=yaml.FullLoader)
        print(f'Загруженные данные равны исходным: {loaded == data}')
