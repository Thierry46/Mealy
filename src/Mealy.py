# -*- coding: utf-8 -*-
"""
*********************************************************
Class  : Mealy.py
Author : Thierry Maillard (TMD)
Date : 1/5/2015 - 10/2/2021

Role : Cipher / decipher a text using a Mealy machine.
Ref : http://philippe.ragout.free.fr/Pages/Cryptographie/Mealy/Presentation.html

Abrev :
TT : Transition Table
TC : Coding Table : letter -> coded letter
TTd : Transition Table for decoding
TCd : Coding Table for decoding

Licence : GPLv3
Copyright (c) 2015 - Thierry Maillard


    This file is part of Mealy project.

    Mealy project is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Mealy project is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Mealy project.  If not, see <http://www.gnu.org/licenses/>.
*********************************************************
"""

import random
import copy
import string

class Mealy:
    """ Cipher / decipher a text using a Mealy machine. """
    def __init__(self, key, config, typeEntity, file="", verbose=False):
        """
        Create a new Mealy machine according parameters :
            - key : the seed value for random numbers generators
            - typeEntity : type of alphabet to use alphabet
            * 'test' -> for shart alphabet 'abcd' for testing
            * 'printable' -> ASCII printable characters extended with
                chars in mealy.ini/MealyMachine/allowedCharsExt
            * 'string' -> 'printable' + letters from string file at the beginning
            * 'file' ->  'printable' + characters found in local file at the beginning
            - verbose : (default False), if True print debug information
        """

        # Test parameters
        if not isinstance(key, int):
            raise ValueError('argument key must be instance of int')
        if not isinstance(typeEntity, str) :
            raise ValueError('argument typeEntity must be instance ' +
                             'of str class')
        if not isinstance(file, str) :
            raise ValueError('argument file must be instance of str class')

        if key < 0:
            raise ValueError(f'Seed for random number generator '
                             f'must be positive : {key}')
        allowedTypeEntity = ('test', 'printable', 'string', 'file')
        if typeEntity not in allowedTypeEntity:
            raise ValueError(f'typeEntity not in {allowedTypeEntity}')

        # Register parameters
        self.key = key
        self.config = config
        self.typeEntity = typeEntity
        self.alphabet = []

        self.nbState = config.getint("MealyMachine", "nbState")
        if self.typeEntity == "test":
            self.nbState = config.getint("MealyMachine", "nbStateTest")
        if self.nbState < 3 :
            raise ValueError('Number of state too low (min 3)'
                             f': {self.nbState}')

        self.file = file
        self.verbose = verbose
        self.TCe = []
        self.TTe = []
        self.TCd = []
        self.TTd = []
        self.ready = False

        if self.verbose :
            print('\nMealy constructor OK :')
            print('key :', self.key)
            print('nbState :', self.nbState)
            print('typeEntity :', self.typeEntity)
            print('file :', self.file)

    def genAlphabetMatrixes(self) :
        """
        Generate alphabet and matrixes,
        must be called before cipher and decipher methods.
        """

        self.alphabet = self.setAlphabet()
        self.setMatrixEncoding()
        self.setMatrixDecoding()
        self.ready = True

    def isReady(self) :
        """ Return True if Mealy machine is ready to be used. """
        return self.ready

    def setAlphabet(self):
        """
        Return alphabet : a list of no duplicate and allowed chars
        allowed chars are given by allowedChars
        or reduced to a small set of chars : test
        only chars in allowedChars string are considered.
        typeEntity and file are used for the order of chars in alphabet :
        put chars of string, a local file or wikipedia's article
        in first position in alphabet

        V3.0 : accept accents in text to cypher
        """

        if self.verbose :
            print('\nsetAlphabet :')
            print('typeEntity :', self.typeEntity)
            print('file :', self.file)

        allowedChars = ("abcd" if self.typeEntity == 'test'
                        else (string.printable +
                        self.config.get("MealyMachine", "allowedCharsExt")))

        # Suppress strange chars that don't work and cause me a lot of problems
        for char in "\x0b\x0c…œæŒÆ\r":
            allowedChars = allowedChars.replace(char, '')

        assert len(allowedChars) > 3, \
               f'alphabet is too tiny : {allowedChars}'
        if len(allowedChars) != len(set(allowedChars)):
            duplicateChars = [char for char in allowedChars
                              if allowedChars.count(char) != 1]
            raise ValueError("Duplicate chars in allowedChars : "
                             f"{duplicateChars}")

        # Page string gives chars to put first in alphabet
        page = ""
        if self.typeEntity in ['file', 'string'] :
            if self.typeEntity == 'file' :
                page = fileReader(self.file, self.verbose)
            else :
                page = self.file

        # Build Alphabet with chars in page first
        lettersInPage = [char for char in page if char in allowedChars]
        lettersInPage.extend(allowedChars)
        alphabet = []
        for char in lettersInPage:
            if char not in alphabet:
                alphabet.extend(char)

        if self.verbose :
            print(f'setAlphabet() : alphabet : {self.alphabet}')
        return alphabet

    def setMatrixEncoding(self):
        """
        Generate coding matrixes : TTe (Transition Table) and TCe (Coding Table)
        according key and alphabet
        """
        if self.verbose :
            print('\nsetMatrixEncoding :')
            print('key :', self.key)
            print('nbState :', self.nbState)
            print('alphabet :', "".join(self.alphabet))

        # Set the seed of random generator to be able to reproduce permutations
        random.seed(self.key)
        nbChar = len(self.alphabet)

        self.TTe = []
        listStateStart = list(range(self.nbState))
        for __ in range(self.nbState):
            listState = []
            for __ in range(nbChar):
                listState.append(random.choice(listStateStart))
            self.TTe.append(listState)

        self.TCe = []
        splittedAlphabet = []
        splittedAlphabet.extend(self.alphabet)
        # ! list() to avoid parameter splittedAlphabet modification
        # if multiple calls of this function
        listChar = list(splittedAlphabet)
        for __ in range(self.nbState) :
            random.shuffle(listChar)
            # ! list() to avoid the copy of the reference only
            self.TCe.append(list(listChar))
        assert len(self.TTe) == len(self.TCe), \
               ('TTe and TCe must have the same number of states : '
                f'(len({self.TTe}) and {len(self.TCe)}')
        assert len(self.TTe) == self.nbState, \
               (f'nbState ({self.nbState}) != '
                f'number of line of matrix {len(self.TTe)})')

        if self.verbose and self.typeEntity == 'test' :
            print('TTe :', self.TTe)
            print('TCe :', self.TCe)

    def getMatrixEncoding(self):
        """
        Return curent encoding matrixes TTe and TCe.
        """
        return self.TTe, self.TCe

    def setMatrixDecoding(self) :
        """
        Generate decoding matrixes : TTd (Transition Table) and TCd (Coding Table) from :
            - TTe : Transition Table used for coding
            - TCe : Coding Table used for coding
            - alphabet : a string representing the allowed alphabet
        """

        if self.verbose :
            print('\nsetMatrixDecoding :')
            if self.typeEntity == 'test' :
                print('alphabet :', "".join(self.alphabet))
                print('TTe :', self.TTe)
                print('TCe :', self.TCe)

        nbChar = len(self.alphabet)
        self.TTd = copy.deepcopy(self.TTe)
        self.TCd = copy.deepcopy(self.TCe)

        for state in range(self.nbState) :
            for indiceChar in range(nbChar) :
                char = self.alphabet[indiceChar]
                codedChar = self.TCe[state][indiceChar]
                try :
                    indiceCodedChar = self.alphabet.index(codedChar)
                except ValueError as exc:
                    raise ValueError(f'Pb decoding : {char} '
                                     'not in allowed alphabet : '
                                     f'{self.alphabet}') from exc
                self.TCd[state][indiceCodedChar] = char
                self.TTd[state][indiceCodedChar] = self.TTe[state][indiceChar]

        if self.verbose and self.typeEntity == 'test':
            print('TTd :', self.TTd)
            print('TCd :', self.TCd)

    def getMatrixDecoding(self):
        """
        Return curent decoding matrixes TTd and TCd.
        """
        return self.TTd, self.TCd

    def cipher(self, text) :
        """
        Cypher a text given in parameter
        """
        if self.verbose :
            print('\ncipher()')

        return _mealy(self.alphabet, self.TTe, self.TCe,
                      text, self.verbose)

    def deCipher(self, text) :
        """
        Cypher a text given in parameter
        """
        if self.verbose :
            print('\ndeCipher()')
        return _mealy(self.alphabet, self.TTd, self.TCd,
                      text, self.verbose)

def fileReader(file, verbose) :
    """
    Get Strings from a file.
    - file :  : local fileName
    - verbose : True if can print debug message.
    V3.0 : encoding = utf8 + context manager (with)
    """
    if verbose :
        print('\nfileReader :')
        print('Name of file to get :', file)

    try :
        with open(file, 'r', encoding='utf8') as infile:
            page = infile.read()
    except IOError as exc:
        raise ValueError(f'Unable to read file {file}') from exc

    if verbose :
        print('Text of file (100 first char) :', file, ':')
        print(page[:100])

    return page

def _mealy(alphabet, TT, TC, text, verbose) :
    """
    Process a text with the Mealy machine
    Parameters :
    - alphabet : allowed characters for text to encode
    - TT and TC : Matrix for state machine
    - verbose : True if can print debug message.
    """
    if verbose :
        print('\n_mealy :')
        print('text :', text[:20], '...')
        if len(alphabet) < 5:
            print('alphabet', alphabet)
            print('TT :', TT)
            print('TC :', TC)

    if not alphabet or not TT or not TC :
        raise ValueError('Mealy machine not ready, alphabet or matrix not set')

    # v3.0 Suppress all characters that are not in alphabet
    textOK = [char for char in text if char in alphabet]

    state = 0
    OutputText = ""
    for char in textOK :
        positionInAlphabet = alphabet.index(char)
        OutputText += TC[state][positionInAlphabet]
        state = TT[state][positionInAlphabet]

    if verbose :
        print('OutputText :', OutputText[:20], '...')
    return OutputText
