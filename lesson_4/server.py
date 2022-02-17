import socket
import argparse
from common.utils import send_message, read_message
from common.variables import MAX_CONNECTIONS, MAX_LENGTH


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
                response = {
                    'response': 202,
                    'alert': f'Привет, {user}!'
                }
            else:
                response = {
                    'response': 401,
                    'alert': 'Пожалуйста, авторизуйтесь'
                }
        else:
            response = {
                'response': 404,
                'error': 'Сообщение не могло быть декодировано'
            }
        print(response)
        send_message(client, response)
        client.close()


if __name__ == '__main__':
    main()
