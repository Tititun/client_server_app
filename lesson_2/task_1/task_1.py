# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
# осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
# info_3.txt и формирующий новый «отчетный» файл в формате CSV


from chardet import detect
import glob
import re
import csv


def get_data(pattern: str):
    """
    функция для поиска изготовителя системы, названия, кода и типа системы в
    текстовых файлах с неизвестной кодировкой.
    Названия файлов должны соответствовать pattern
    Результат - список из списков с данными, первый список представляет
    собой заголовки
    """
    manufs, names, codes, types = [], [], [], []
    reg_dict = {
        re.compile(r'Изготовитель системы:\s*([^\r\n]*)'): manufs,
        re.compile(r'Название ОС:\s*([^\r\n]*)'): names,
        re.compile(r'Код продукта:\s*([^\r\n]*)'): codes,
        re.compile(r'Тип системы:\s*([^\r\n]*)'): types,
    }
    for file in glob.glob(pattern):
        with open(file, 'rb') as f:
            content = f.read()
            encoding = detect(content)['encoding']
            text = content.decode(encoding)
        for reg, arr in reg_dict.items():
            match = reg.search(text)
            arr.append(match.groups()[0] if match else '')
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта',
                 'Тип системы']]
    for manuf, name, code, t in zip(manufs, names, codes, types):
        main_data.append([manuf, name, code, t])
    return main_data


def write_to_csv(file_name, pattern):
    """
    функция собирает данные из файлов (при помощи функции get_data(pattern))
    соответствующих названию pattern и записывает собранные данные в
    csv файл file_name
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        data = get_data(pattern)
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    write_to_csv('task_1_result.csv', 'data/info_*.txt')
