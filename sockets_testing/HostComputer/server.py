import socket

HOST = '192.168.1.1' # My computer's IP
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created!")

try:
    s.bind((HOST,PORT))
except socket.error:
    print("Error")
    quit()


s.listen(1)
print("Server awaiting messages")
conn, addr = s.accept()
print("Connected")


while True:
    data = conn.recv(1024)
    print("I sent a message in response to: ", data.decode())


    # Process Data
    if data == bytes("Hello", 'utf-8'):
        reply = "Hello Client!"
    elif data == bytes("quit", 'utf-8'):
        conn.send(bytes('Terminating','utf-8'))
        break
    else:
        reply = "Unknown Command"

    # Sending Reply

    conn.send(bytes(reply,'utf-8'))
conn.close()
