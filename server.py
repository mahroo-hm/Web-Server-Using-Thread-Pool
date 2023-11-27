import socket
import concurrent.futures
import signal
import os
import uuid  # For generating unique IDs

SERVER_ADDRESS = ('localhost', 8080)
MAX_THREADS = 5


def process_request(client_socket, request):
    try:
        method, path = request.split(' ')

        if method != 'GET':
            send_error_response(client_socket, '400', 'INVALID METHOD')
            return

        if not path.startswith('/'):
            send_error_response(client_socket, '400', 'INVALID PATH')
            return

        filename = path[1:]
        if not os.path.exists(filename):
            send_error_response(client_socket, '404', 'FILE DOES NOT EXISTS')
            return

        with open(filename, 'rt') as file:
            while True:
                content = file.read(1024)
                if not content:
                    break
                client_socket.send(str(content).encode('ascii'))

    except Exception as e:
        print('Error processing request:', e)
        send_error_response(client_socket, '500', 'INTERNAL SERVER ERROR')


def send_error_response(client_socket, code, message):
    response = 'STAT' + code + ' | ' + message
    client_socket.sendall(response.encode('ascii'))


def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode('ascii')
    print(request)
    process_request(client_socket, request)
    client_socket.close()


def signal_handler(signal, frame):
    print('Received SIGINT signal, shutting down server...')
    executor.shutdown()
    server_socket.close()
    exit(1)


signal.signal(signal.SIGINT, signal_handler)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(0)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS)

while True:
    print('Waiting for connection...')
    client_socket, address = server_socket.accept()
    if client_socket is None:
        continue
    appointment_no = str(uuid.uuid4())
    response = f"STAT 200 | APPOINMENT NUMBER: {appointment_no}".encode('ascii')
    client_socket.sendall(response)
    print('Accepted connection from:', address)

    if executor._max_workers - len(executor._threads) == 0:
        send_error_response(client_socket, '503', 'THREADPOOL IS FULL')
        client_socket.close()
    else:
        executor.submit(handle_client_connection, client_socket)