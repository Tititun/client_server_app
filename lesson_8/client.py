import random
import socket
from common.variables import MAX_LENGTH
from common.utils import send_message, read_message
import time
import argparse
import logging
from decorators import log
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
    parser.add_argument('mode', type=str, help='отправлять или слушать')
    parser.add_argument('-u', '--user', type=str, help='имя пользователя',
                        nargs='?', default='Guest')
    args = parser.parse_args()
    if args.mode not in ['send', 'listen']:
        logger.error(f'mode должен быть listen или send, получено {args.mode}')
        return

    logger.debug('Скрипт запущен с запросом на соединение с сервером '
                 f'{args.address}:{args.port} от пользователя {args.user}'
                 f'Мод: {args.mode}')

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.address, args.port))

        if args.mode == 'send':
            message_text = random.choice(['корова', 'собака', 'курица'])
            message = {
                'action': 'message',
                'time': time.time(),
                'message': message_text,
                'user': {
                    'account_name': args.user,
                    'status': 'online'
                }
            }
            logger.info(f'Отправляется сообщение: {message_text}')
            send_message(client, message)
        elif args.mode == 'listen':
            while True:
                data = client.recv(MAX_LENGTH)
                if msg := read_message(data):
                    chat_message = parse_message(msg)
                    logger.info(f'Сообщение в чате: {chat_message}')

        client.close()

    except ConnectionError:
        logger.error(f'Не удалось установить соединение с сервером '
                     f'{args.address}:{args.port}')


if __name__ == '__main__':
    main()
