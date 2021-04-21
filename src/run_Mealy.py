#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
*********************************************************
Programme run_Mealy.py
Auteur : Thierry Maillard (TMD)
Date : 15/5/2015 - 1/4/2021

Role : Launch ciphering or deciphering with a Mealy machine.

Parameters : without -b parameter, run GUI
    -h or --help : display this help.
    -v or --verbose : set debug mode On
    batch :
    -b or --batch : Batch mode
    -n or --numkey= value : numeric key (int)
    -s or --stringkey= text : text string used as key
    -f or --filekey= name : local file name used as key
    -i or --inputFile= name : local file name containing text to process
    -t or --text= string containing text to process
    -o or --outputFile= name : local file name where result is written
    -d or --decipher : decipher text, else cipher

Licence : GPLv3
Copyright (c) 2015 - 2021 - Thierry Maillard


    This file is part of Mealy project.

    Mealy project is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later.

    Mealy project is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Mealy project.  If not, see <http://www.gnu.org/licenses/>.
*********************************************************
"""

import sys
# Minimum version for Python
assert sys.version_info >= (3,6)

import configparser
import getopt
import gettext
import locale
import os
import os.path
import platform

import MealyGUI
import Mealy


def main(argv=None):
    """
    Main function for batch or GUI mode
    return code for oprating system.
    0 if OK
    """

    cr = 0

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    verbose = False
    batchMode = False
    numKey = 0
    fileKey = ""
    stringKey = ""
    inputFile = ""
    outputFile = ""
    textString = ""
    cipher = True
    typeEntity = "printable"

    locale.setlocale(locale.LC_ALL, '')
    localeDirPath = os.path.join(os.path.dirname(sys.argv[0]),
                                 config.get('Resources', 'LocaleDir'))
    gettext.install(config.get('Resources', 'MessageNameFile'),
                    localeDirPath)

    if argv is None:
        argv = sys.argv

    # parse command line options
    try:
        opts, __ = getopt.getopt(
            argv[1:],
            "hVvbdn:s:f:i:t:o:",
            ["help", "version", "verbose", "batch", "decipher",
             "numkey", "stringkey", "filekey",
             "inputfile", "text", "outputfile"]
            )
    except getopt.error as msg:
        print(msg)
        print("To get help use --help ou -h")
        cr = 1

    # process options
    for option, arg in opts:
        if option in ("-h", "--help"):
            print(__doc__)
            cr = -1
            break

        if option in ("-V", "--version"):
            print("Version :", \
                config.get('Version', 'appName'), \
                config.get('Version', 'number'), \
                config.get('Version', 'date'))
            cr = -1
            break

        if option in ("-v", "--verbose"):
            verbose = True
        if option in ("-b", "--batch"):
            batchMode = True
        if option in ("-n", "--numkey"):
            numKey = int(arg.strip())
        if option in ("-s", "--stringkey"):
            stringKey = arg.strip()
            typeEntity = "string"
            fileKey = stringKey
        if option in ("-f", "--filekey"):
            fileKey = arg.strip()
            typeEntity = "file"
        if option in ("-i", "--inputfile"):
            inputFile = arg.strip()
        if option in ("-o", "--outputfile"):
            outputFile = arg.strip()
        if option in ("-t", "--text"):
            textString = arg.strip()
        if option in ("-d", "--decipher"):
            cipher = False

    print('Start', \
        config.get('Version', 'appName'), \
        config.get('Version', 'number'), \
        config.get('Version', 'date'))
    if verbose:
        print('Parameters :')
        print('--verbose : verbose mode On')
        if batchMode:
            print('--batch : Batch mode')
            print('--numkey=', numKey)
            if stringKey:
                print('--stringkey=', fileKey)
            if fileKey:
                print('--fileKey=', fileKey)
            print('--inputFile=', inputFile)
            print('--text=', textString)
            print('--outputFile=', outputFile)
            if cipher:
                print('cipher')
            else:
                print('--decipher : decipher')
        else:
            print('GUI mode...')

    # Check options compatibility
    if batchMode and ((inputFile and textString) or not (inputFile or textString)):
        print("Please choose an uniq way to enter text for ciphering\n",
              "-i and -t options are exclusive !")
        cr = -1

    # Do the job
    if cr == 0:
        if batchMode :
            text = textString
            if inputFile:
                with open(inputFile, 'r', encoding='utf8') as infile:
                    if verbose :
                        print(f'Reading text from : {inputFile}')
                    text = infile.read()
            cr = runBatch(verbose, config,
                          numKey, typeEntity, fileKey,
                          cipher, text, outputFile)
        else : # GUI Mode
            MealyGUI.runGUI(verbose, config)

    print('End run_Mealy.py')
    return cr

def runBatch(verbose, config,
            numKey, typeEntity, fileKey,
            cipher, text, outputFile):
    '''
    runBatch :
    run Mealy machine in batch according given parameters
    V3.0 : encoding = utf8 + context manager (with)
    return 0 if conversion OK
    '''

    cr = 0
    mealy = Mealy.Mealy(numKey, config, typeEntity, fileKey, verbose)
    mealy.genAlphabetMatrixes()

    if mealy.isReady():
        # Do the job
        if cipher :
            print('Cyphering...')
            result = mealy.cipher(text)
        else :
            print('Deciphering...')
            result = mealy.deCipher(text)
    else :
        print("mealy machine not initialized")
        cr = 1

    if not cr:
        try:
            with open(outputFile, 'w', encoding='utf8') as outfile:
                if verbose :
                    print(f'Writing result in : {outputFile}...')
                outfile.write(result)
                print('Ok : text processed and written '
                      f'in {outputFile}')
        except FileNotFoundError as exc:
            print(f'Problem : {outputFile} can not be opened :\n{exc}')
            cr = 1

    return cr

##################################################
#to be called as a script
if __name__ == "__main__":
    returnCode = main()
    sys.exit(returnCode)
