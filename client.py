import socket

SERVER_ADDRESS = ('localhost', 8080)


def handle_response(resp):
    print(resp)
    status_code, message = resp.split(' ', 1)
    if status_code == '200':
        print(message)
    else:
        print('Error:' + status_code + '(' + message + ')')


cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_socket.connect(SERVER_ADDRESS)
cl_id = cl_socket.recv(1024).decode()
print(cl_id)

while True:
    req = 'GET /bib.txt'
    cl_socket.send(req.encode('ascii'))
    resp = cl_socket.recv(1024)
    if not resp:
        break
    print(resp.decode('ascii'))
cl_socket.close()