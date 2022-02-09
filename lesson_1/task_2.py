# 2. Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode
# и decode) и определить тип, содержимое и длину соответствующих переменных.


def value_summary(word):
    """функця для записи переменной в байтовый тип и вывода типа, содержимого
     и длины переменной"""
    try:
        byte_word = eval(f'b"{word}"')
    except SyntaxError:
        print(f'{word} не может быть конвертировано в байты данным способом')
        return
    print(f'Вводные данные: {word}')
    print(f'Тип полученной переменной: {type(byte_word)}')
    print(f'Содержимое: {byte_word}')
    print(f'Длина: {len(byte_word)}')
    print('------------------')


if __name__ == '__main__':
    for word in ['class', 'function', 'method']:
        value_summary(word)
