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


while True: # Server Menu Loop
    data = conn.recv(4096)  # Recives message at the start of every loop. This message controls the response
    print("I sent a message in response to: ", data.decode())

    temp_loop = True
    # Process Data
    if data.decode() == '1':    # Print the part list
        attempt = ""
        for i in range(len(parts_list)):    # Loops through the part list, adds it to a string, and then sends the data
            attempt += "--------------------------------------------------------------------------------\n"
            attempt += str(parts_list[i].part_number) + " " + str(parts_list[i].part_name) + "\n"
            attempt += str(parts_list[i].description) + "\n"

            # family type conversion
            if (parts_list[i].family == 0): attempt += "TTL" + "\n"
            elif (parts_list[i].family == 1): attempt += "BiCMOS" + "\n"
            elif (parts_list[i].family == 2): attempt += "CMOS" + "\n"
            else: print("ERROR ",end="")

            # package type conversion
            if (parts_list[i].package == 0): attempt += "SSOP"  + "\n"
            elif (parts_list[i].package == 1): attempt += "SOIC " + "\n"
            elif (parts_list[i].package == 2): attempt += "DIP" + "\n"
            elif (parts_list[i].package == 3): attempt += "CFP"  + "\n"
            elif (parts_list[i].package == 4): attempt += "LCCC" + "\n"
            elif (parts_list[i].package == 5): attempt += "SO" + "\n"
            else: print("ERROR")

            # Vcc conversion
            for i in range(4):
                if(parts_list[i].vcc[i] != 0.0):
                    attempt += str(parts_list[i].vcc[i]) + "V"
                    if(i == 0 and (parts_list[i].vcc[1] != 0.0 or parts_list[i].vcc[2] != 0.0 or parts_list[i].vcc[3] !=0.0)):
                        attempt += ", "
                    if(i == 1 and (parts_list[i].vcc[2] != 0.0 or parts_list[i].vcc[3] !=0.0)):
                        attempt += ", "
                    if(i == 2 and (parts_list[i].vcc[3] !=0.0)):
                        attempt += ", "
            
            attempt += "\n"
        
        reply = attempt
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == '2':  # Print a specific part number
        #reply = "print part"
        search = conn.recv(4096).decode()
        print(search)
        found = False
        attempt = ""
        for i in range(len(parts_list)):    # searches for a part and adds it to the list
            if(parts_list[i].getPartNumber() == search):
                attempt += "\n--------------------------------------------------------------------------------\n"
                attempt += str(parts_list[i].part_number) + " " + str(parts_list[i].part_name) + "\n"
                attempt += str(parts_list[i].description) + "\n"

                 # family type conversion
                if (parts_list[i].family == 0): attempt += "TTL" + "\n"
                elif (parts_list[i].family == 1): attempt += "BiCMOS" + "\n"
                elif (parts_list[i].family == 2): attempt += "CMOS" + "\n"
                else: print("ERROR ",end="")

                # package type conversion
                if (parts_list[i].package == 0): attempt += "SSOP"  + "\n"
                elif (parts_list[i].package == 1): attempt += "SOIC " + "\n"
                elif (parts_list[i].package == 2): attempt += "DIP" + "\n"
                elif (parts_list[i].package == 3): attempt += "CFP"  + "\n"
                elif (parts_list[i].package == 4): attempt += "LCCC" + "\n"
                elif (parts_list[i].package == 5): attempt += "SO" + "\n"
                else: print("ERROR")

                # Vcc conversion
                for i in range(4):
                    if(parts_list[i].vcc[i] != 0.0):
                        attempt += str(parts_list[i].vcc[i]) + "V"
                        if(i == 0 and (parts_list[i].vcc[1] != 0.0 or parts_list[i].vcc[2] != 0.0 or parts_list[i].vcc[3] !=0.0)):
                            attempt += ", "
                        if(i == 1 and (parts_list[i].vcc[2] != 0.0 or parts_list[i].vcc[3] !=0.0)):
                            attempt += ", "
                        if(i == 2 and (parts_list[i].vcc[3] !=0.0)):
                            attempt += ", "
                
                attempt += "\n"
                
                reply = str(attempt)
                #print(reply)
                found = True
                conn.send(bytes(reply,'utf-8'))
        if(found == False):
            reply = "\nCould not find part\n"
            print(reply)
            conn.send(bytes(reply,'utf-8'))
            continue
    elif data.decode() == '3':  # Add a part to the list
        new_part = "" # Temp string to recive data
        while(new_part == ""): # Waits to recive the data
            new_part = conn.recv(1024).decode()

        # Adds data into temp object
        part = SNx4xx.SNx4xx()
        new_part = new_part.split("\n")
        part.setPartNumber(new_part[0])
        part.setPartName(new_part[1])
        part.setDescription(new_part[2])
        part.setFamily(new_part[3])
        part.setPackage(new_part[4])
        part.setVcc(new_part[5])
        parts_list.append(part) # Adds to the parts list
        #reply = "Part added!"
    elif data.decode() == '4':  # Sort the list by part number
        parts_list.sort(key=lambda x: x.part_number)
        reply = "List is sorted!"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == '5':  # Save the list
        file_name = "outfile.part" # outfile name
        write_object = open(file_name, 'w') # opens file
        for obj in parts_list: # loops and writes all object data into file
            obj.write(write_object)
        write_object.close()
        print("List is saved in " + file_name)
        reply = "List is saved to server!"
        conn.send(bytes(reply,'utf-8'))
    elif data.decode() == "6": # Quits
        conn.send(bytes('Terminating','utf-8'))
        break
    else:
        reply = "Unknown Command"
        conn.send(bytes(reply,'utf-8'))

    # Sending Reply

    #conn.send(bytes(reply,'utf-8'))
conn.close()
