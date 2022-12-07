import socket

HOST = '192.168.1.1'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))


while True:
    command = bytes(input('Enter your command: '), 'utf-8')
    s.send(command)
    reply = s.recv(1024)
    if reply == bytes('Terminating','utf-8'):
        break
    print(reply)