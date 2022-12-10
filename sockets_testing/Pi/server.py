import socket
import SNx4xx

# Ip and Host info and creates socket
HOST = '192.168.1.23' # My computer's IP
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created!")

# Tries to bind with socket.
try:
    s.bind((HOST,PORT))
except socket.error:
    print("Error")
    quit()

# Connects to Client
s.listen(1)
print("Server awaiting messages")
conn, addr = s.accept()
print("Connected")

################## Class testing/data ##################
# Variable
infile = "infile2.part" # File name
parts_list = [] # list of parts
running = True # bool value for menu loop

# Opens file, creates list of lines, and cleans list
try:
    file_object = open(infile,'r')
    lines = file_object.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
except:
    msg = "File:" + infile + " cannot be opened"
    print(msg)
    exit()

# Loads in data from infile and puts them into a list
count = 0
loop = True
while(loop):
    temp = SNx4xx.SNx4xx() # Temp object for loading into parts list
    if(temp.load(lines,count) == False):
        loop = False
        break
    parts_list.append(temp)
    count += 1
########################################################

while True:
    data = conn.recv(1024)
    print("I sent a message in response to: ", data.decode())

    temp_loop = True
    # Process Data
    if data.decode() == '1':    # Print the part list
        reply = "Part Number\nPart Name\nPart family\nPart package\nPart Vcc\ndone"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == '2':  # Print a specific part number
        reply = "print part"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == '3':  # Add a part to the list
        reply = "add part"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == '4':  # Sort the list by part number
        reply = "sort list"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == '5':  # Sort the list by part number
        reply = "save list"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == "6":
        conn.send(bytes('Terminating','utf-8'))
        break
    else:
        reply = "Unknown Command"
        conn.send(bytes(reply,'utf-8'))

    # Sending Reply

    #conn.send(bytes(reply,'utf-8'))
conn.close()
