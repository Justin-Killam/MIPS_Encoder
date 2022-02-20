"""
Filename: MIPS_Decoder.py
Author: Justin Killam
Description: A python script that reads the context of a text
that is placed in the same folder as the .py file. The contents
of the file are a series of MIPS instructions in a particular 
format. Once read the script converts the instructions into 
there machine code counterparts in both binary and hexadecimal
format, and then outputs them to two seperate files. This allows
for easy conversion of MIPS code into something readable by 
verilogs readmem compiler directive. All of the instructions
are provided to the user in a preamble that is displayed before
they are prompted to enter their file name. 
"""

"""
Function Definitions
"""

#Function for reading and parsing the MIPS code
def File_Read(fileName):
    fileObj=open(fileName,"r")
    fileText=fileObj.read()
    fileObj.close()
    codeFormatted=[]
    codeLines=fileText.split("\n")
    for line in codeLines:
        codeFormatted.append(line.split(" "))
    return codeFormatted

#Function for looking up register names
def registerLookUp(regName):
    if ('$'in regName):
        regVal=registerLookUp.register_names.index(regName)
    else:
        regVal=int(regName);
    return format(regVal,"05b")
registerLookUp.register_names=["$0","$at","$v0","$v1","$a0","$a1","$a2","$a3","$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7","$t8","$t9","$k0","$k1","$gp","$sp","$fp","$ra"]


def instructionLookUp(instruction):
    if(instruction in instructionLookUp.instruction_names):
        index_found=instructionLookUp.instruction_names.index(instruction)
        opcode=instructionLookUp.opcodes[index_found]
        function=instructionLookUp.functions[index_found]
        return [opcode,function]
    else:
        return ["X","X"]

instructionLookUp.instruction_names=["lw","sw","add","sub","addu","subu","and","or","xor","sll","srl","sra","sllv","srlv","srav","j","beq","bne","addi","addiu","andi","ori","xori"]
instructionLookUp.opcodes=["100011","101011","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000000","000010","000100","000101","001000","001001","001100","001101","001110"]
instructionLookUp.functions=["000000","000000","100000","100010","100001","100011","100100","100101",  "100110"  ,"000000","000010","000011","000100","000110","000111","000000","000000","000000","000000","000000","000000","000000","000000"]

#Generating the binary string for the immediates
def ImmGen(imm,formatspec):
    imm=int(imm)
    if(imm<0):
        SeImm=((-1*imm)^0x0000ffff)+1
    else:
        SeImm=imm
    return format(SeImm,formatspec)
    
def MIPS_Encode(CodeArray):
    machineCode=[]
    for line in CodeArray:
        current_instruction=line[0]
        [opcode,function]=instructionLookUp(current_instruction)
        #R-Type    
        if(opcode=="000000"):
            rdBin=registerLookUp(line[1])
            #note for constant its rd rt shamt: and s=0
            if(current_instruction in ["sll","srl","sra"]):
                rtBin=registerLookUp(line[2])
                rsBin="00000"
                shamtBin=format(int(line[3]),"05b")
            #note for variable shift operations its rd rt rs: and shamt=0
            elif(current_instruction in["sllv","srlv","srav"]):
                rtBin=registerLookUp(line[2])
                rsBin=registerLookUp(line[3])
                shamtBin="00000"
            #note for normal r-type its rd rs rt: and shamt=0
            else:
                rsBin=registerLookUp(line[2])
                rtBin=registerLookUp(line[3])
                shamtBin="00000"
            machineCode.append(opcode+rsBin+rtBin+rdBin+shamtBin+function)        
        #J-Type
        elif(opcode=="000010"):
            machineCode.append(opcode+ImmGen(line[1],"026b"))
        #I-Type
        else:
            #lw,sw is rt imm rs 
            if(line[0] in ["lw","sw"]):
                rtBin=registerLookUp(line[1])
                immBin=ImmGen(line[2],"016b")
                rsBin=registerLookUp(line[3])
            #beq,bne is rs rt imm
            elif(line[0]in["beq","bne"]):
                rsBin=registerLookUp(line[1])
                rtBin=registerLookUp(line[2])
                immBin=ImmGen(line[3],"016b")
            #normal i type is rt rs imm 
            else:
                rtBin=registerLookUp(line[1])
                rsBin=registerLookUp(line[2])
                immBin=ImmGen(line[3],"016b")
            machineCode.append(opcode+rsBin+rtBin+immBin)
    return machineCode

def fileWrite(machineCode):
    fileObj1=open("MachineCode_Bin.txt","w")
    fileObj2=open("MachineCode_Hex.txt","w")
    for codeline in machineCode:
        codehex=format(int(codeline,2),"08x")
        fileObj1.write(codeline+"\n")
        fileObj2.write(codehex+"\n")
    fileObj1.close()
    fileObj2.close()




header="""
                    MIPS to Bin/Hex Converter
---------------------------------------------------------------------
*********************************************************************
    Below are all commands  supported by the Converter

    Note1: All constants will be represented by 5 as all
    constants are represented in signed decimal.

    Note2: Register names or numbers can be used. If using
    names prefix the name with $  ex: $t0

    Note3: Seperate arguements by spaces and arguements with
    parenthesis should  have the parenthesis omited
*********************************************************************
    lw $rt 5 $rs
    sw $rt 5 $rs
    add $rd $rs $rt
    sub $rd $rs $rt
    addu $rd $rs $rt
    subu $rd $rs $rt
    and $rd $rs $rt
    or $rd $rs $rt
    xor $rd $rs $rt
    sll $rd $rt 5
    srl $rd $rt 5
    sra $rd $rt 5
    sllv $rd $rt $rs
    srlv $rd $rt $rs
    srav $rd $rt $rs
    j 5
    beq $rs $rt 5
    bne $rs $rt 5
    addi $rt $rs 5
    addiu $rt $rs 5
    andi $rt $rs 5
    ori $rt $rs 5
    xori $rt $rs 5
---------------------------------------------------------------------


"""

print(header)

#reading from a user specified input file
inFile=input("Enter File extension:")
code=File_Read(inFile)
machineCode=MIPS_Encode(code)
fileWrite(machineCode)