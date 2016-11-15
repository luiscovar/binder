#include <string>
#include "codearray.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <vector>
#include <sys/stat.h>
#include <sys/types.h>

using namespace std;

int main()
{
    
    /* The child process id */
    pid_t childProcId = -1;
        
    /* Go through the binaries */
    for(int progCount = 0; progCount < NUM_BINARIES; ++progCount)
    {
        char *fileName = tmpnam(NULL);
        FILE *temp = fopen(fileName, "wb");
            
        //Open the file and write the bytes of the first program to the file.
        if(fwrite(codeArray[progCount], sizeof(char), programLengths[progCount], temp) < 0)
        {
            perror("fwrite");
            exit(-1);
        }

        fclose(temp);
            
        
        //Make the file executable
        chmod(fileName, 0777);
        
        
        //Create a child process using fork
        childProcId = fork();
    
        /* I am a child process; I will turn into an executable */
        if(childProcId == 0)
        {
            // use execlp() in order to turn the child process into the process
            //running the program in the above file.
            if(execlp(fileName, "file", NULL) < 0)
            {
                perror("execlp");
                exit(-1);
            }
        
        }
        else if(childProcId < 0)
        {
            fprintf(stderr, "Fork Failed");
            exit(-1);
        }
    }
    
    /* Wait for all programs to finish */
    for(int progCount = 0; progCount < NUM_BINARIES; ++progCount)
    {
        /* Wait for one of the programs to finish */
        if(wait(NULL) < 0)
        {
            perror("wait");
            exit(-1);
        }    
    }
}
