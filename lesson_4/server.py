import socket
import re
import argparse
from common.utils import send_message, read_message
from common.variables import MAX_CONNECTIONS, MAX_LENGTH


def compile_response(status, message, type_):
    return {
        'response': status,
        type_: message
    }


def check_ip_port(ip, port):
    """
    функция проверяет, чтобы ip соответствовал ipv4 формату и порт
    был в  пределах допустимых значений
    """
    ip_match = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
    port_match = port < 65535
    return ip_match and port_match


def main():
    """
    Запускает работу сервера с аргументами из командной строки:
    -a --address - ip адрес сервера, дефолтное значние: 127.0.0.1
    -p --port - порт для прослушивания, дефолтное значние: 8888
    Сервер читает полученное сообщение и отправляет ответ
    """
    parser = argparse.ArgumentParser(description='Скрипт для получения'
                                                 'presence сообщений')
    parser.add_argument('-a', '--address',  type=str, help='ip адрес сервера',
                        default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, help='порт сервера',
                        default=8888)
    args = parser.parse_args()
    if not check_ip_port(args.address, args.port):
        print('Убедитесь, что ip адрес указан верно и порт < 65535')
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((args.address, args.port))
    s.listen(MAX_CONNECTIONS)

    while True:
        client, addr = s.accept()
        print(f'Получен запрос на соединение от {addr}')
        data = client.recv(MAX_LENGTH)
        msg = read_message(data)
        print(msg)
        if msg:
            user = msg.get('user', {}).get('account_name', 'Аноним')
            if msg.get('action') == 'presence':
                response = compile_response(202, f'Привет, {user}!', 'alert')
            else:
                response = compile_response(401, 'Пожалуйста, авторизуйтесь',
                                            'alert')
        else:
            response = compile_response(404, 'Сообщение не могло'
                                             ' быть декодировано', 'error')
        print(response)
        send_message(client, response)
        client.close()


if __name__ == '__main__':
    main()
