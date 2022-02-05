# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
# преобразовать результаты из байтовового в строковый тип на кириллице.

# большая часть кода взята с урока, поскольку задание аналогичное

import chardet
import subprocess
import platform


def ping_resource(resource):
    """
    :param resource: вебсайт для пингования. Например: 'google.com'
    :return: выводит результат в консоль, преобразуя из байтового типа в
     строковый, ничего не возвращает
    """
    print(f'Пингуем вебсайт: {resource}\n Результат:')
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', resource]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in result.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


if __name__ == '__main__':
    for website in ['yandex.ru', 'youtube.com']:
        ping_resource(website)
