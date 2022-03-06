import select
import socket
import re
import argparse
import time

from common.utils import send_message, read_message
from common.variables import MAX_CONNECTIONS, MAX_LENGTH
import logging
from decorators import log
from log.server_log_config import server_logger

logger = logging.getLogger('server_logger')


@log
def compile_response(status, message, type_):
    # logger.debug(f'функция compile_response вызвана с параметрами'
    #              f' status: {status}, message: {message}, type_: {type_}')
    return {
        'response': status,
        type_: message
    }


@log
def check_ip_port(ip, port):
    """
    функция проверяет, чтобы ip соответствовал ipv4 формату и порт
    был в  пределах допустимых значений
    """
    # logger.debug(f'функция check_ip_port вызвана с параметрами'
    #              f' ip: {ip}, port: {port}')
    ip_match = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
    port_match = port < 65535
    return ip_match and port_match

@log
def process_message(rec, users, socket_):
    """
    функция обрабатывает сообщение формирует ответ
    """
    message = read_message(rec)
    response = {}
    if message:
        action = message.get('action')
        user = message.get('user', {}).get('account_name', 'Guest')
        if action == 'presence':
            response['message'] = f'Пользователь {user} присоединился к чату'
            users[user] = socket_
        elif action == 'message':
            response['from'] = user
            response['message'] = message.get('message')
            response['to'] = message.get('to')
        response['status'] = 200
        response['time'] = time.time()
    return response

@log
def delete_user(user: socket, users_dict: dict):
    """
    удаляет пользователя из списка активных пользователей
    """
    for name, socket_ in users_dict.items():
        if socket_ == user:
            del users_dict[name]
            break

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
    logger.debug(f'Сервер запущен с параметрами: ip - {args.address}'
                 f' port - {args.port}')
    if not check_ip_port(args.address, args.port):
        logger.error(f'Сервер {args.address}:{args.port} не удалось запустить')
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((args.address, args.port))
    s.settimeout(1)
    s.listen(MAX_CONNECTIONS)

    clients = []
    users = {}

    while True:
        try:
            client, addr = s.accept()
            logger.info(f'Получен запрос на соединение от {addr}')
        except OSError:
            pass
        else:
            clients.append(client)
            logger.info(f'Установлено соединение с {client}')

        recieved, listeners, err = [], [], []
        try:
            if clients:
                recieved, listeners, err = select.select(clients, clients,
                                                         [], 0)
        except:
            continue

        logger.info(f'Получено {len(recieved)} сообщений')
        messages = []   # собираем все полученные сообщения
        print('Пользователи:', users)
        if recieved:
            for rec in recieved:
                try:
                    message = rec.recv(MAX_LENGTH)
                    if message == b'':
                        raise Exception
                    if msg := process_message(message, users, rec):
                        messages.append(msg)
                except:
                    delete_user(rec, users)
                    if rec in clients:
                        clients.remove(rec)

        # если сообщения есть, то отправляем их всем слушающим пользователям:
        logger.info(f'{len(listeners)} пользователей ожидают сообщения')
        for listener in listeners:
            try:
                for message in messages:
                    to = message.get('to')
                    if to and users.get(to) != listener:
                        continue
                    logger.info(f'Отправляется сообщение {message}')
                    send_message(listener, message)
            except:
                # клиент отсоединился
                delete_user(listener, users)
                clients.remove(listener)


if __name__ == '__main__':
    main()
