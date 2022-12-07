import SNx4xx

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

while(running): # Menu loop
    print("Enter option:")
    print("		(1) Print the part list")
    print("		(2) Print a specific part number")
    print("		(3) Add a part to the list")
    print("		(4) Sort the list by part number")
    print("		(5) Save the list")
    print("		(6) Exit the program")
    case = input("				Choice ?")
    if(case == '1'):
        for i in range(len(parts_list)):
            parts_list[i].print()
    elif(case == '2'):
        found = False
        search = input("Enter full part number to find: ")
        print("")
        for i in range(len(parts_list)):
            if(parts_list[i].getPartNumber() == search):
                parts_list[i].print()
                found = True
        if(found == False):
            print("Could not find part")
    elif(case == '3'):
        part = SNx4xx.SNx4xx()
        part.setPartNumber(input("Enter Part Number (ex. SN7415N): "))
        part.setPartName(input("Enter Part Name (ex. Triple 3 Input NAND gate): "))
        part.setDescription(input("Enter Part Description: "))
        if(part.setFamily(input("Enter Part Family (i.e., TTL, BiCMOS, CMOS): "))): continue
        if(part.setPackage(input("Enter Part Package (i.e., SSOP, SOIC, DIP, CFP, LCCC, SO): "))): continue
        if(part.setVcc(input("Enter VCC Options (must be 4 numbers i.e., 3.3 2.5 1.8 0.0): "))): continue
        parts_list.append(part)
    elif(case == '4'):
        parts_list.sort(key=lambda x: x.part_number)
    elif(case == '5'):
        write_object = open("outfile.part", 'w')
        for obj in parts_list:
            obj.write(write_object)
        write_object.close()
    elif(case == '6'):
        running = False