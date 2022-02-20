import socket
from common.variables import MAX_LENGTH
from common.utils import send_message, read_message
import time
import argparse


def create_presence(send_to: socket.socket,
                    user: str = 'guest',
                    status: str = 'online'):
    """функция для отправки presence сообщения на сервер"""
    msg = {
        'action': 'presence',
        'time': time.time(),
        'user': {
            'account_name': user,
            'status': status
        }
    }
    send_message(send_to, msg)


def main():
    """
    Отправляет presence сообщение на сервер
    Работает позиционными аргументами из командной строки:
    -address - ip адрес сервера, обязательный аргумент
    -port - порт сервера, стандартное значние: 8888
    -u --user опциональный аргумент, имя пользователя,
                                     стандартное значние: Guest

    """
    parser = argparse.ArgumentParser(description='Скрипт для отправки presence'
                                                 ' сообщения и чтения ответа')
    parser.add_argument('address', type=str, help='ip адрес сервера')
    parser.add_argument('port', type=int, help='порт сервера', nargs='?',
                        default=8888)
    parser.add_argument('-u', '--user', type=str, help='имя пользователя',
                        nargs='?', default='Guest')
    args = parser.parse_args()

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.address, args.port))

        create_presence(client, args.user)
        data = client.recv(MAX_LENGTH)
        msg = read_message(data)
        if msg:
            print(f'Получен ответ от сервера с кодом {msg["response"]}:')
            for response_type in ['alert', 'error']:
                if response := msg.get(response_type):
                    print(response)
        else:
            print('Ответ сервера не мог быть декодирован')

        client.close()
    except ConnectionError:
        print(f'Не удалось установить соединение с сервером '
              f'{args.address}:{args.port}')


if __name__ == '__main__':
    main()
