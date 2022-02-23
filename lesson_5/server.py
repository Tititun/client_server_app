import socket
import re
import argparse
from common.utils import send_message, read_message
from common.variables import MAX_CONNECTIONS, MAX_LENGTH
import logging
from log.server_log_config import server_logger

logger = logging.getLogger('server_logger')


def compile_response(status, message, type_):
    logger.debug(f'функция compile_response вызвана с параметрами'
                 f' status: {status}, message: {message}, type_: {type_}')
    return {
        'response': status,
        type_: message
    }


def check_ip_port(ip, port):
    """
    функция проверяет, чтобы ip соответствовал ipv4 формату и порт
    был в  пределах допустимых значений
    """
    logger.debug(f'функция check_ip_port вызвана с параметрами'
                 f' ip: {ip}, port: {port}')
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
    logger.debug(f'Сервер запущен с параметрами: ip - {args.address}'
                 f' port - {args.port}')
    if not check_ip_port(args.address, args.port):
        logger.error(f'Сервер {args.address}:{args.port} не удалось запустить')
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((args.address, args.port))
    s.listen(MAX_CONNECTIONS)

    while True:
        client, addr = s.accept()
        logger.info(f'Получен запрос на соединение от {addr}')
        data = client.recv(MAX_LENGTH)
        msg = read_message(data)
        logger.info(f'Получено сообщение от {addr}: {msg}')
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
        send_message(client, response)
        logger.info(f'Отправлен ответ для {addr}: {response}')
        client.close()


if __name__ == '__main__':
    main()
