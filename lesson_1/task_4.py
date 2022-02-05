# 4. Преобразовать слова «разработка», «администрирование»,
# «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

def to_bytes_and_back(word, encoding='utf-8'):
    """
    функция преобразует word в байты и обратно и выводит
    полученные значения
    """
    print(f'Исходное слово: {word}')
    word_bytes = word.encode(encoding)
    print(f'Преобразованное слово: {word_bytes}')
    word_back = word_bytes.decode(encoding)
    print(f'Обратное преобразование: {word_back}')
    print('-----------------------')


if __name__ == '__main__':
    for word in ['администрирование', 'протокол', 'стандарт']:
        to_bytes_and_back(word)
