#Reading and splitting up the code file
def File_Read(fileName):
    fileObj=open(fileName,"r")
    fileText=fileObj.read()
    fileObj.close()
    codeFormatted=[]
    codeLines=fileText.split("\n")
    for line in codeLines:
        codeFormatted.append(line.split(" "))
    return codeFormatted

#looking up the register names and generating their binary
def registerLookUp(regList,regName):
    if ('$'in regName):
        regVal=regList.index(regName)
    else:
        regVal=int(regName);
    return format(regVal,"05b")

#Generating the binary string for the immediates
def immGen(imm,formatspec):
    imm=int(imm)
    if(imm<0):
        SeImm=((-1*imm)^0x0000ffff)+1
    else:
        SeImm=imm
    return format(SeImm,formatspec)

#look up arrays for register names, instruction names, opcodes, and functions
register_names=["$0","$at","$v0","$v1","$a0","$a1","$a2","$a3","$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7","$t8","$t9","$k0","$k1","$gp","$sp","$fp","$ra"]
instruction_names=["lw","sw","add","sub","addu","subu","and","or","xor","sll","srl","sra","sllv","srlv","srav","j","beq","bne","addi","addiu","andi","ori","xori"]
opcodes=["100011","101011","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000010","000100","000101","001000","001001","001100","001101","001110"]
functions=["000000","000000","100000","100010","100001","100011","100100","100101",  "100110"  ,"000000","000010","000011","000100","000110","000111","000000","000000","000000","000000","000000","000000","000000","000000"]

#reading from a user specified input file
inFile=input("Enter File extension:")
inFile="C:\Users\killa\Documents\Python_Projects\New folder\CodeSample.txt"
code=File_Read(inFile)

machineCode=[]
for line in code:
    arrayLoc=instruction_names.index(line[0])
    opcode=opcodes[arrayLoc]
    function=functions[arrayLoc]
    #R-Type
    
    
    
    if(opcode=="000000"):
        rdBin=registerLookUp(register_names,line[1])
        #note for constant its rd rt shamt: and s=0
        if(line[0]in ["sll","srl","sra"]):
            rtBin=registerLookUp(register_names,line[2]);
            rsBin="00000"
            shamtBin=format(int(line[3],"05b")
        #note for variable shift operations its rd rt rs: and shamt=0
        elif(line[0]in["sllv","srlv","srav"]):
            rtBin=registerLookUp(register_names,line[2]);
            rsBin=registerLookUp(register_names,line[3]);
            shamtBin="00000"
        #note for normal r-type its rd rs rt: and shamt=0
        else:
            rsBin=registerLookUp(register_names,line[2]);
            rtBin=registerLookUp(register_names,line[3]);
            shamtBin="00000";
        machineCode.append(opcode+rsBin+rtBin+rdBin+shamt+funct)        
    #J-Type
    elif(opcode=="000010"):
        machineCode.append(opcode+immGen(line[2],"026b"))
    #I-Type
    else:
        #lw,sw is rt imm rs 
        if(line[0] in ["lw","sw"]):
            rtBin=registerLookUp(register_names,line[1])
            immBin=immGen(line[2],"016b")
            rsBin=registerLookUp(register_names,line[3])
        #beq,bne is rs rt imm
        elif(line[0]in["beq","bne"]):
            rsBin=registerLookUp(register_names,line[1])
            rtBin=registerLookUp(register_names,line[2])
            immBin=immGen(line[3],"016b")
        #normal i type is rt rs imm 
        else:
            rtBin=registerLookUp(register_names,line[1])
            rsBin=registerLookUp(register_names,line[2])
            immBin=immGen(line[3],"016b")
        machineCode.append(opcode+rsBin+rtBin+immBin)
    