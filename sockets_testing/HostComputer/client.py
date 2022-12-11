import socket
import time

#test

# Ip and Host info and creates socket
HOST = '192.168.1.23'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))  # Connects socket with server.py

# Class Variables for correct Package and Family types
FAMILY_ASSERT = ["TTL", "BiCMOS", "CMOS"]
PACKAGE_ASSERT = ["SSOP", "SOIC", "DIP", "CFP", "LCCC", "SO"]


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

    #Menu 1 - Print list of parts


    # Menu 3 - Add a part to the list
    if(command.decode() == '3'):
        add_object = ""
        # Intakes Part Number and Name
        add_object += input("Enter Part Number (ex. SN7415N): ") + "\n"
        add_object += input("Enter Part Name (ex. Triple 3 Input NAND gate): ") + "\n"
        
        # Intakes family and checks if input is valid
        temp_family = input("Enter Part Family (i.e., TTL, BiCMOS, CMOS): ")
        if(temp_family in FAMILY_ASSERT):   # Asserts
            add_object += temp_family + "\n"
        else:
            print("\nPlease enter a correct family.\n")
            continue
        
        # Intakes package and checks if input is valid
        temp_package = input("Enter Part Package (i.e., SSOP, SOIC, DIP, CFP, LCCC, SO): ")
        if(temp_package in PACKAGE_ASSERT): # Asserts
            add_object += temp_package + "\n"
        else:
            print("\nPlease enter a correct package.\n")
            continue
        
        # Intakes Vcc and checks if input is valid
        temp_vcc = input("Enter VCC Options (must be 4 numbers i.e., 3.3 2.5 1.8 0.0): ")
        try:
            temp = temp_vcc.split() # Splits the Vcc string up
            assert len(temp) == 4   # Checks for 4 numbers
            temp = [float(a) for a in temp] # Checks if floating type
            add_object += temp_vcc  # Adds to add_object
        except: # Fail handler
            print("\nPlease enter Vcc numbers in correct format.\n")
            continue

        print(add_object)


    reply = s.recv(4096)
    if reply.decode() == 'Terminating':
        break
    print(reply.decode())