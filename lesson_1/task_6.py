# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Далее забыть о том, что
# мы сами только что создали этот файл и исходить из того, что перед нами файл
# в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости
# от того, в какой кодировке он был создан.

from chardet import detect

text_file = 'test_file.txt'
with open(text_file, 'w') as f:
    f.write(f'сетевое программирование\nсокет\nдекоратор')


# Первый вариант: проверить кодировку перед декодированием:
with open(text_file, 'rb') as f:
    text_bytes = f.read()
    encoding = detect(text_bytes)['encoding']
    text = text_bytes.decode(encoding)
    print(text)


# Второй вариант, открыть в такой кодировке, в какой хотим, проигнорировав
# все неизвестные нашей кодировке символы
with open(text_file, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()
    print(text)
