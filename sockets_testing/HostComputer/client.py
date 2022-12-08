import socket
import time

HOST = '192.168.1.23'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))


while True:
    # Menu Print
    print("Enter option:")
    print("		(1) Print the part list")
    print("		(2) Print a specific part number")
    print("		(3) Add a part to the list")
    print("		(4) Sort the list by part number")
    print("		(5) Save the list")
    print("		(6) Exit the program")

    # Intakes command and sends to server
    command = bytes(input("				Choice ?"), 'utf-8')
    s.send(command)

    # Menu 1 (Working, but a bit finicky. Sometimes only prints out some of the data.)
    if(command.decode == '1'):
        Looping = True  # Bool for looping until all are printed
        while Looping:
            time.sleep(1)   # added a time delay to see if it will fix^
            reply = s.recv(1024).decode()
            print(reply)
            if(reply == "done"):
                s.send(bytes("done",'utf-8'))
                Looping = False
        
        break



    reply = s.recv(1024)
    if reply.decode() == 'Terminating':
        break
    print(reply.decode())