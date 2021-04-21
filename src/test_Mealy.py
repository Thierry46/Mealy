# coding: utf-8
"""
Name : test_mealy
Author : Thierry Maillard (TMD)
Date : 1/5/2015 - 8/2/2021
Role : Unit testing of mealy project with py.test
Usage : py.test .
    ou pour être sur d'utiliser Python 3 :
    python3 -m pytest .
        options :
        -s : to see stdout output
        -k xxx : to run only xxx test case

Ref : http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-3/
Ref : http://pytest.org/latest/
prerequis : pip3 install pytest

Licence : GPLv3
Copyright (c) 2021 - Thierry Maillard

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
"""

import configparser

import pytest
import Mealy

@pytest.mark.parametrize("key, typeEntity, file", [
    (-1, 'test', ''),
    (1, '', ''),
    ([1], 'test', ''),
    (1, 2, ''),
    (1, 'test', 3)
    ])
def test_Mealy_pb_param(key, typeEntity, file):
    """ Test bad parameters """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    with pytest.raises(ValueError):
        Mealy.Mealy(key, config, typeEntity, file)

def test_fileReader_BadName():
    """ Test filereader with unknown filename """

    with pytest.raises(ValueError):
        Mealy.fileReader('XYZXYZ', True)

def test_fileReader_OK() :
    """ Test filereader with filename OK"""

    page = Mealy.fileReader("Mealy.py", True)
    assert len(page) > 100, f'Less than 100 char got from page :\n{page}'

@pytest.mark.parametrize("typeEntity,file", [
    ("file", "XYZXYZ"),
    ("file", "."),
    ])
def test_setAlphabet_pbparam(typeEntity,file):
    """ Test setAlphabet with parameters problems for file or wikipedia """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    mealy = Mealy.Mealy(key, config, typeEntity, file)
    with pytest.raises(ValueError):
        mealy.setAlphabet()

def test_Mealy_setAlphabet_test():
    """ Test very small test alphabet """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = "test"
    mealy = Mealy.Mealy(key, config, typeEntity)
    assert mealy.setAlphabet() == list("abcd")

def test_Mealy_setAlphabet_printable():
    """ Test real alphabet extended with config """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = "printable"
    allowedChars = ("0123456789" +
                        "abcdefghijklmnopqrstuvwxyz" +
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n") + \
                    config.get("MealyMachine", "allowedCharsExt")

    mealy = Mealy.Mealy(key, config, typeEntity)
    assert mealy.setAlphabet() == list(allowedChars)


@pytest.mark.parametrize("typeEntity,file", [
    ("file", "Mealy.py"),
    ("string","zx"),
    ("string","zz")
    ])
def test_setAlphabet_OK_file_string(typeEntity,file):
    """
    Test real alphabet extended with config
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    allowedChars = ("0123456789" +
                        "abcdefghijklmnopqrstuvwxyz" +
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n") + \
                   config.get("MealyMachine", "allowedCharsExt")

    mealy = Mealy.Mealy(key, config, typeEntity, file)
    alphabet = mealy.setAlphabet()

    assert len(alphabet) == len(allowedChars), 'Problem with alphabet size'
    for char in alphabet:
        assert char in allowedChars, f'char {char} not in allowedChars'
        assert alphabet.count(char) == 1, f'duplicated char {char} in alphabet'

def test_setAlphabet_order_file():
    """
    Test real alphabet extended with config
    and a file for setting aplphabet order
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = "string"
    file = "thierry"
    allowedChars = ("0123456789" +
                        "abcdefghijklmnopqrstuvwxyz" +
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n") + \
                   config.get("MealyMachine", "allowedCharsExt")

    mealy = Mealy.Mealy(key, config, typeEntity, file)
    alphabet = mealy.setAlphabet()

    assert len(alphabet) == len(allowedChars)
    assert "".join(alphabet).startswith("thiery")

def test_Mealy_setAlphabet_equal_2_runs():
    """
    Test real alphabet extended with config
    are same for two differen runs.
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = "printable"

    mealy1 = Mealy.Mealy(key, config, typeEntity)
    alphabetRun1 = mealy1.setAlphabet()
    mealy2 = Mealy.Mealy(key, config, typeEntity)
    alphabetRun2 = mealy2.setAlphabet()
    assert alphabetRun1 == alphabetRun2

def test_matrix_equals_2_runs_same_args():
    """
    Test if cyphering and decyphering matrix are the same
    for 2 different run with same ciphering parameters.
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = 'test'
    nbState = config.getint("MealyMachine", "nbStateTest")
    mealy1 = Mealy.Mealy(key, config, typeEntity)
    mealy1.genAlphabetMatrixes()
    TT1,TC1 = mealy1.getMatrixEncoding()

    mealy2 = Mealy.Mealy(key, config, typeEntity)
    mealy2.genAlphabetMatrixes()
    TT2,TC2 = mealy2.getMatrixEncoding()
    assert TT1 == TT2, 'incorrect with same args : TT run1 != TT run2'
    assert TC1 == TC2, 'incorrect with same args : TC run1 != TC run2'
    assert len(TT1) == nbState, 'Bad number of line in TT1'
    assert len(TC1) == nbState, 'Bad number of line in TC1'

def test_matrix_different_2_runs_different_keys():
    """
    Test if cyphering and decyphering matrix are different
    for 2 different run with different ciphering parameters.
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key1 = 1
    key2 = 2
    nbState = config.getint("MealyMachine", "nbState")
    typeEntity = 'string'
    mealy1 = Mealy.Mealy(key1, config, typeEntity)
    mealy1.genAlphabetMatrixes()
    TT1,TC1 = mealy1.getMatrixEncoding()
    mealy2 = Mealy.Mealy(key2, config, typeEntity)
    mealy2.genAlphabetMatrixes()
    TT2,TC2 = mealy2.getMatrixEncoding()
    assert TC1 != TC2, 'incorrect with different args : TC run1 == TC run2'
    assert len(TC1) == nbState, 'Bad number of line in TC1'
    assert len(TC1) == len(TC2), 'Different number of line bitwenn TC1 and TC2'
    assert len(TT1) == len(TT2), 'Different number of line bitwenn TT1 and TT2'

def test_matrix_code_decode_different():
    """
    Test if cyphering and decyphering matrix are different
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = 'test'
    mealy = Mealy.Mealy(key, config, typeEntity)
    mealy.genAlphabetMatrixes()
    TT,TC = mealy.getMatrixEncoding()
    TTd,TCd = mealy.getMatrixDecoding()
    assert TT != TTd, 'TT Coding and decoding matrixes must be differents : TT == TTd'
    assert TC != TCd, 'TC Coding and decoding matrixes must be differents : TC == TCd'

def testMealyTextNotInAlphabet():
    """
    Test cyphering text with unknown characters in alphabetAlphabet for tests is abcd
    e letter must be discarded in result.
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = 'test'
    text = "aed"

    mealy = Mealy.Mealy(key, config, typeEntity)
    mealy.genAlphabetMatrixes()
    assert mealy.isReady(), 'Flag ready not True'

    # Test coding and decoding
    mealy.verbose = True
    cryptedText = mealy.cipher(text)
    assert text != cryptedText, 'Pb : text == cryptedText !'

    # Test decoding
    decodedText = mealy.deCipher(cryptedText)
    assert decodedText == "ad", 'Text after cephering/decephering != ad'

@pytest.mark.parametrize("text", ['ab', 'abc', 'abcd'])
def testMealySimple(text):
    """
    Alphabet is abcd : too short :
    some ciphered sequence can be the same as other
    Next test is more representative
    """
    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 1
    typeEntity = 'test'

    mealy = Mealy.Mealy(key, config, typeEntity)
    mealy.genAlphabetMatrixes()
    assert mealy.isReady(), 'Flag ready not True'

    # Test coding and decoding
    mealy.verbose = True
    cryptedText = mealy.cipher(text)
    assert text != cryptedText, 'Pb : text == cryptedText !'

    # Test decoding
    decodedText = mealy.deCipher(cryptedText)
    assert text == decodedText, 'Text after cephering/decephering is different'

@pytest.mark.parametrize("inputText", ["", "a", "Salut tout le monde !",
                                   "ligne 1\nligne 2",
                                   "àãáâÀÃÁÂéèêëÉÈÊËîïÎÏùüûÙÜÛôöÔÖ",
                                       "hello secret"])
def test_Mealy_Full(inputText):
    """
    Test cyphering and decyphering on text with different
    char classes.
    """

    # read project properties
    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    key = 123
    typeEntity = 'printable'

    mealy = Mealy.Mealy(key, config, typeEntity)
    mealy.genAlphabetMatrixes()
    assert mealy.isReady(), 'Flag ready not True'

    # Test coding
    cryptedText = mealy.cipher(inputText)
    if inputText != '' :
        assert inputText != cryptedText, 'Pb : input == cryptedText !'

    # Test decoding
    decodedText = mealy.deCipher(cryptedText)
    assert inputText == decodedText
