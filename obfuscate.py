#!/usr/bin/python3

import argparse
import string
import random

batchLetterDictionary = []
batchCommandDictionary = []
codeLineMixerDictionary = []
obfuscatedCommandDictionary = []
class graphics:
    runBanner = """
                                     __________
                              ______/ ________ \______
                            _/      ____________      \_
                          _/____________    ____________\_
                         /  ___________ \  / ___________  \\
                        /  /XXXXXXXXXXX\ \/ /XXXXXXXXXXX\  \\
                       /  /############/    \############\  \\
                       |  \XXXXXXXXXXX/ _  _ \XXXXXXXXXXX/  |
                     __|\_____   ___   //  \\   ___   _____/|__
                     [_       \     \  X    X  /     /       _]
                     __|     \ \                    / /     |__
                     [____  \ \ \   ____________   / / /  ____]
                          \  \ \ \/||.||.||.||.||\/ / /  /
                           \_ \ \  ||.||.||.||.||  / / _/
                             \ \   ||.||.||.||.||   / /
                              \_   ||_||_||_||_||   _/
                                \     ........     /
                                 \________________/"""
    information = """
#####################################################################################
###################         TrickBot Batch Obfuscator             ###################
################### Author: SlizBinksman                          ###################
################### Note: Author Not Responsible For Your Actions.###################
################### GitHub: https://github.com/slizbinksman       ###################
#####################################################################################
"""

    description = """Batch obfuscator based on a huntress article about the obfuscation used by the trickbot launcher.
Author is absolutely not responsible for the users actions.
Huntress article: https://blog.huntresslabs.com/tried-and-true-hacker-technique-dos-obfuscation-400b57cd7dd
Usage: python3 obfuscate.py my_batch_file.bat obfuscated.bat 10
"""

    def printBanner(self):
        print(graphics.runBanner)

class arguments:

    parser = argparse.ArgumentParser(description=graphics().description,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('InputFile',type=str,help='Batch file to obfuscate')
    parser.add_argument('OutputFile',type=str,help='Obfuscated file name')
    parser.add_argument('--quiet','-q',action='store_true',help='Turn Off Banner')
    args = parser.parse_args()

class scrambler:

    def scrambleVar(self,batchVar):
        letters = string.ascii_letters
        args = arguments().args
        self.scrambled = (''.join(random.choice(letters) for i in range(1, 7)))
        if batchVar == True:
            self.obfuscatedVar = f'%{self.scrambled}%'
            return self.obfuscatedVar
        else:
            return self.scrambled

class fileio:

    global setVariable, spaceVariable, equalSignVariable

    def checkForExtension(self,file):
        splitFile = file.split('.')
        if splitFile[1] != 'bat':
            exit('[!] Error. Batch File Not Detected.')
        else:
            print('[*] Batch File Detected. Continuing')

    def getBatchCode(self,inputfile):
        print(f'[*] Reading {inputfile}. Storing Code In Dictionary')
        with open(inputfile,'r') as fileInput:
            batchCode = fileInput.read()
            singleBatchCommand = batchCode.split('\n')
            batchCommandDictionary.append(singleBatchCommand)
            fileInput.close()
            return batchCode

    def startObfuscation(self,inputFile,outputFile):
        print('[*] Starting Obfuscation Process')
        self.checkForExtension(inputFile)
        def setVariableEqualTo(variable, value):
            code = f'{setVariable}{spaceVariable}{variable}{equalSignVariable}{value}'
            batchList = [f'%{variable}%',value]
            batchLetterDictionary.append(batchList)
            return code

        setVariable = scrambler().scrambleVar(batchVar=False)
        spaceVariable = scrambler().scrambleVar(batchVar=False)
        equalSignVariable = scrambler().scrambleVar(batchVar=False)
        print(f'[*] Writing Initial Set Variables To {outputFile}')
        with open(outputFile,'w') as outputFile:
            outputFile.write(f'set {setVariable}=set\n')
            setVariable = f'%{setVariable}%'
            outputFile.write(f'{setVariable} {spaceVariable}= \n')
            spaceVariable = f'%{spaceVariable}%'
            outputFile.write(f'{setVariable}{spaceVariable}{equalSignVariable}==\n')
            equalSignVariable = f'%{equalSignVariable}%'
            batchCode = fileio().getBatchCode(inputFile)

            print('[*] Writing Set Variables To File')
            for letter in batchCode:
                outputFile.write(f'{setVariableEqualTo(scrambler().scrambleVar(batchVar=False),letter)}\n')

            print(f'[*] Writing Variables From Dictionary')
            for variable in batchLetterDictionary:
                if variable[1] == '\n':
                    outputFile.write('\n')
                else:
                    outputFile.write(str(variable[0]))
            outputFile.close()

    def mixUpLines(self,OutputFile):
        print('[*] Mixing Set Variables For Further Obfuscation')
        with open(OutputFile,'r') as file:
            setVariableCode = file.readlines()
            file.close()
        for line in setVariableCode:
            if len(line) == 32:
                codeLineMixerDictionary.append(line)

        mixedSetVariables = random.sample(codeLineMixerDictionary,len(codeLineMixerDictionary))

        print('[*] Finishing Obfuscation Process')
        with open(OutputFile,'w') as file:
            file.write('@echo off\n')
            for obfuscatedLine in setVariableCode[0:3]:
                file.write(obfuscatedLine)
            for obfuscatedLine in mixedSetVariables:
                file.write(obfuscatedLine)
            for obfuscatedLine in setVariableCode[len(mixedSetVariables)+3:]:
                file.write(obfuscatedLine)
            file.close()

class program:

    def launch(self):
        arg = arguments().args
        if not arg.quiet:
            graphics().printBanner()
        print(graphics.information)
        fileio().startObfuscation(arg.InputFile,arg.OutputFile)
        fileio().mixUpLines(arg.OutputFile)
        exit(f'[*] Finished Obfuscation Process. Obfuscated Batch File Saved As {arg.OutputFile}')

if __name__ == '__main__':
    program().launch()