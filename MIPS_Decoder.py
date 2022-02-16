def File_Read(fileName):
    fileObj=open(fileName,"r")
    fileText=fileObj.read()
    fileObj.close()
    codeFormatted=[]
    codeLines=fileText.split("\n")
    for line in codeLines:
        codeFormatted.append(line.split(" "))
    return codeFormatted

#lookups
register_names=[]
instruction_names=["lw","sw"]
opcodes=[]
function=[]

#reading from a user specified input file
inFile=input("Enter File extension:")
inFile="C:\Users\killa\Documents\Python_Projects\New folder\CodeSample.txt"
code=File_Read(inFile)

for line in code:
    arrayLoc=instruction_names.index(line[0])
    
    #R-Type
    if(opcodes=="000000"):
    
    #J-Type
    elif(opcodes=="000010"):
    
    #I-Type
    else: