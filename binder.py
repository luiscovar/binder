import os
import sys
import subprocess
from subprocess import call, check_call
import os
from subprocess import Popen, PIPE

FILE_NAME = "codearray.h";

#get the hex bytes of the passed in files
def getHexDump(execPath):
    retVal = None
    hexdump = Popen(["hexdump", "-v", "-e", '"0x" 1/1 "%02X" ","', execPath], stdout=PIPE)
    # 1. Use popen() in order to run hexdump and grab the hexadecimal bytes of the program.
    output, err = hexdump.communicate()
    exit_code = hexdump.wait()
    if exit_code == 0:
        retVal = str(output).split(",")
    return retVal

#generate the codearray.h file
def generateFile(execList, fileName, progCount):
    programLen = []
    headerFile = open(fileName, "w")
    headerFile.write("#include <string>\n\nusing namespace std;\n\nunsigned char* codeArray["+str(progCount)+"] = {");
    
    for count, progName in enumerate(execList):
            hexdump = getHexDump(progName)
            hexLen = len(hexdump) - 1
            programLen.append(hexLen)
            headerFile.write("\nnew unsigned char["+str(hexLen)+"] {")
            if count != progCount - 1:
                headerFile.write(",".join(map(str, hexdump[:-1])) + "},")
            else:
                headerFile.write(",".join(map(str, hexdump[:-1])) + "}")
    headerFile.write("\n};\n")

    # Add array to containing program lengths to the header file
    headerFile.write("\n\nunsigned programLengths[] = {" +",".join(map(str,programLen)) + "};\n")
    # define the number of programs
    headerFile.write("\n\n#define NUM_BINARIES " +  str(progCount))
    
    # Close the file
    headerFile.close()

#Compile the file
def compileFile(binderCppFileName, execName):
    print("Compiling...")
    try:
        subprocess.check_call(["g++", binderCppFileName , "-o", execName, "-std=gnu++11"])
        print "Compilation succeeded"
    except subprocess.CalledProcessError:
        print "Compilation Failed"

def main():
    progNames = sys.argv[1:]
    progCount = len(progNames)
    generateFile(progNames, FILE_NAME, progCount)
    compileFile("binderbackend.cpp", "bound")

if __name__ == '__main__':
    main()
