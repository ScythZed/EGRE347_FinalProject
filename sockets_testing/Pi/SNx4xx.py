class SNx4xx:

    '''
     def __init__() 
    
     Summary of function: 
            constructor for SNx4xx
    
     Parameters     Part Number : The part's number naming convention.
            	    Part Name 	: The part's name, normally with notable gate orientation.
            		Description : Discribes the part, usually a longer line of text describing it.
            		Family 		: An Enum data type defining what type the logic family.
            		Package 	: An Enum data type defining what package type the part is from.
            		Vcc 		: An array of up to 4 supply voltages that the part can use.
    
     Return Value : N/A
    '''
    def __init__(self, part_number="SNx4xx", part_name="NONE", description="NONE", family=0, package=0, vcc=[0.0, 0.0, 0.0, 0.0]):
        self.part_number = part_number
        self.part_name = part_name
        self.description = description
        self.family = family
        self.package = package
        self.vcc = vcc

    '''
     def load() 
    
     Summary of function: 
            loads in data from text file lines. Returns True if everything loads.
            If load fails/reaches the end, it will return false.
    
     Parameters   : lines:   list of lines created in main from infile
                  : count:   count of how many times the load function has happened
                             and off sets reading from lines based on this number
    
     Return Value : Returns True if everything loads.
                    If load fails/reaches the end, it will return false.    
    '''
    def load(self, lines, count):
        count *= 6
        try:
            self.part_number = lines[count]
            self.part_name = lines[count + 1]
            self.description = lines[count + 2]
            self.family = int(lines[count + 3])
            self.package = int(lines[count + 4])
            temp = lines[count + 5].split()
            for i in range(len(temp)):
                temp[i] = float(temp[i])
            self.vcc = temp
            return True
        except:
            return False

    '''
     Data Member Getters 
    
     Summary of function: 
            returns respective data member 
    '''
    def getPartNumber(self):
        return self.part_number
    
    def getPartName(self):
        return self.part_name
    
    def getDescription(self):
        return self.description
    
    def getFamily(self):
        return self.family
    
    def getPackage(self):
        return self.package

    def getVcc(self):
        return self.vcc

    '''
     Data Member Getters 
    
     Summary of function: 
            returns respective data member
     Note:
        Family and Package sets the respective int value and check if parameter passed is valid.
        If not, it prints a message and returns false. Else, they return true.
        Vcc does the same thing, but it also type converts from string to float.
    '''
    def setPartNumber(self, value):
        self.part_number = value
    
    def setPartName(self, value):
        self.part_name = value
    
    def setDescription(self, value):
        self.description = value
    
    def setFamily(self, value):
        if(value == "TTL"): temp = 0
        elif(value == "BiCMOS"): temp = 1
        elif(value == "CMOS"): temp = 2
        else:
            print("\nPlease enter a correct family.\n")
            return True
        self.family = temp
        return False
    
    def setPackage(self, value):
        if(value == "SSOP"): temp = 0
        elif(value == "SOIC"): temp = 1
        elif(value == "DIP"): temp = 2
        elif(value == "CFP"): temp = 3
        elif(value == "LCCC"): temp = 4
        elif(value == "SO"): temp = 5
        else:
            print("\nPlease enter a correct package.\n")
            return True
        self.package = temp
        return False

    def setVcc(self, value):
        try:
            temp = value.split()
            assert len(temp) == 4
            temp = [float(a) for a in temp]
            self.vcc = temp
            return False
        except:
            print("\nPlease enter Vcc numbers in correct format.\n")
            return True


    '''
     def print() 
    
     Summary of function: 
            prints object as defined in Hw 4/5
    
     Parameters   : None.
    
     Return Value : None.   
    '''
    def print(self):
        print("--------------------------------------------------------------------------------")
        print(self.part_number + " " + self.part_name)
        print(self.description + "\n")

        if (self.family == 0): print("TTL ",end="")
        elif (self.family == 1): print("BiCMOS ",end="")
        elif (self.family == 2): print("CMOS ",end="")
        else: print("ERROR ",end="")

        if (self.package == 0): print("SSOP")
        elif (self.package == 1): print("SOIC ")
        elif (self.package == 2): print("DIP")
        elif (self.package == 3): print("CFP")
        elif (self.package == 4): print("LCCC")
        elif (self.package == 5): print("SO")
        else: print("ERROR")

        for i in range(4):
            if(self.vcc[i] != 0.0):
                print(str(self.vcc[i]) + "V",end="")
                if(i == 0 and (self.vcc[1] != 0.0 or self.vcc[2] != 0.0 or self.vcc[3] !=0.0)):
                    print(", ",end="")
                if(i == 1 and (self.vcc[2] != 0.0 or self.vcc[3] !=0.0)):
                    print(", ",end="")
                if(i == 2 and (self.vcc[3] !=0.0)):
                    print(", ",end="")
        
        print("\n")

    '''
     def write() 
    
     Summary of function: 
            writes data into the parameter file, which is opened in main
    
     Parameters   : file : file object to be written to
    
     Return Value : None.   
    '''
    def write(self,file):
        list = []
        list += (str(self.part_number) + "\n")
        list += (str(self.part_name) + "\n")
        list += (str(self.description) + "\n")
        list += (str(self.family) + "\n")
        list += (str(self.package) + "\n")
        temp = ""
        for value in self.vcc: temp += (str(value) + " ")
        list += (temp + "\n")
        file.writelines(list)
        return