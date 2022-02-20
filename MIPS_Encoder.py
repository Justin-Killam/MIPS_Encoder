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
        if(line !=""):
            codeFormatted.append(line.split(" "))
    return codeFormatted

#Function for catching displaying errors detected in file formating    
def Error_Display(msg):
    input("Error!!! "+msg+"\nHit enter or close the window...")
    exit()

#Function for looking up register names
def registerLookUp(regName):
    if (regName in registerLookUp.register_names):
        regVal=registerLookUp.register_names.index(regName)
    elif(regName.isdecimal()):
        regVal=int(regName);
    else:
       Error_Display("Register name or number invalid!!! Check that it is in the proper format.") 
    return format(regVal,"05b")
registerLookUp.register_names=["$0","$at","$v0","$v1","$a0","$a1","$a2","$a3","$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7","$t8","$t9","$k0","$k1","$gp","$sp","$fp","$ra"]

#Function for looking up instruction code
def instructionLookUp(instruction):
    if(instruction in instructionLookUp.instruction_names):
        index_found=instructionLookUp.instruction_names.index(instruction)
        opcode=instructionLookUp.opcodes[index_found]
        function=instructionLookUp.functions[index_found]
        return [opcode,function]
    else:
        Error_Display("Instruction does not exist!!! Check that it is in the proper format.")

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

#Function for encoding the contents of the code file    
def MIPS_Encode(CodeArray):
    machineCode=[]
    for line in CodeArray:
        current_instruction=line[0]
        if(current_instruction not in ["nop","NOP"]):    
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
        else:
            machineCode.append(format(0,"032b"))
    return machineCode

#Function for writing the results to the hex and binary files
def fileWrite(machineCode):
    fileObj1=open("MachineCode_Bin.txt","w")
    fileObj2=open("MachineCode_Hex.txt","w")
    for codeline in machineCode:
        codehex=format(int(codeline,2),"08x")
        fileObj1.write(codeline+"\n")
        fileObj2.write(codehex+"\n")
    fileObj1.close()
    fileObj2.close()


#Preamble header

header="""
                            MIPS to Bin/Hex Converter
-----------------------------------------------------------------------------------
***********************************************************************************
                                Instructions
    1.  The format for the code file should be ".txt"
    2.  Each instruction should be on its own line.
    3.  All letters should be lower case.
    4.  Instructions and arguements should be seperated by only 1 space each
    5.  If using register names prefix them with "$" ex "$t0", but when
        using the number do not ex for RF location 8 use "8". 
        Note:Location zero is either "0" or "$0"
    6.  For memory access instructions like lw and sw the order of the
        arguements is maintained but the parenthesis should not be included.
        ex: lw $t0 1 $0 rather than lw $t0 1($0)
    7.  All constants should be represented in signed decimal ex "5" or "-5"
    8.  Once the code is finished and formated it can be placed in the same
        file location as the "MIPS_Decoder.py" file.
    9.  Enter the file name (ex:TestFile.txt) where prompted below, and hit
        enter to start the encoding
    10. You will now either have your coverted files in the same location or
        and error message becasue the code was formatted incorrectly
    
     (Below is a list of supported instructions and their associated formats)
 (If you downloaded this off of the git hub there should be an example code file)
***********************************************************************************
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
    nop
-----------------------------------------------------------------------------------


"""

print(header)

#reading from a user specified input file
inFile=input("Enter File extension:")
code=File_Read(inFile)
machineCode=MIPS_Encode(code)
fileWrite(machineCode)
input("Encoding Completed. You may hit enter to exit, or simply close the window.")