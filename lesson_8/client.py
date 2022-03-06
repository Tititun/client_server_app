import socket
from common.variables import MAX_LENGTH
from common.utils import send_message, read_message
import time
import argparse
import logging
from decorators import log
import threading
from log.client_log_config import client_logger

logger = logging.getLogger('client_logger')


@log
def create_presence(send_to,
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


@log
def is_response_success(status_code):
    """
    функция для проверки статуса ответа от сервера
    """
    if 300 >= status_code >= 100:
        return True
    else:
        return False

@log
def parse_message(msg):
    from_ = msg.get('from', 'Чат-бот')
    message = msg.get('message')
    return f'{from_}: {message}'


def receive_message(client):
    """
    функция, которая печатает полученное сообщение
    """
    while True:
        data = client.recv(MAX_LENGTH)
        if msg := read_message(data):
            chat_message = parse_message(msg)
            print(f'Сообщение в чате: {chat_message}')


def user_thread(client, user):
    """
    функция запрашивает у пользователя имя получателя и сообщение,
    затем отправляет сообщение
    """
    print(f'Добро пожаловать в чат. Для выхода нажмите Ctrl + C')
    while True:
        to = input('Введите получателя:\n')
        message_text = input('Введите текст сообщения:\n')
        message = {
            'action': 'message',
            'time': time.time(),
            'message': message_text,
            'to': to,
            'user': {
                'account_name': user,
                'status': 'online'
            }
        }
        logger.info(f'Отправляется сообщение ({user}): {message_text}')
        send_message(client, message)


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

    logger.debug('Скрипт запущен с запросом на соединение с сервером '
                 f'{args.address}:{args.port} от пользователя {args.user}')

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.address, args.port))
        create_presence(client, user=args.user)

        listen_thread = threading.Thread(target=receive_message, args=(client,))
        listen_thread.daemon = True
        listen_thread.start()

        send_thread = threading.Thread(target=user_thread, args=(client,
                                                                 args.user))
        send_thread.daemon = True
        send_thread.start()

        while True:
            time.sleep(0.5)
            if listen_thread.is_alive() and send_thread.is_alive():
                continue
            break

    except ConnectionError:
        logger.error(f'Не удалось установить соединение с сервером '
                     f'{args.address}:{args.port}')


if __name__ == '__main__':
    main()
