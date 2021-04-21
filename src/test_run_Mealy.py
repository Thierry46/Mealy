# coding: utf-8
"""
Name : test_run_Mealy
Author : Thierry Maillard (TMD)
Date : 1/2/2021 - 6/2/2021
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

import os
import os.path
import configparser
import difflib

import pytest

import run_Mealy

@pytest.mark.parametrize( "verbose", [True, False])
def test_batch_cypher_decypher_simple_textfile(verbose):
    """ Simple batch ciphering / decyphering """

    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    pathTest = config.get('Test', 'run_Mealy.path_test')
    print("pathOutput directory =", pathTest)

    # Check test environment
    assert os.path.isdir(pathTest), f"First create {pathTest} dir !"
    pathTestFile = os.path.join(pathTest,
                                config.get('Test', 'run_Mealy.test_file'))
    assert os.path.isfile(pathTestFile), f"{pathTestFile} must exist"
    pathTestFileResult = os.path.join(pathTest,
                                      config.get('Test',
                                                 'run_Mealy.test_file_result'))
    pathTestFileDecode = os.path.join(pathTest,
                                      config.get('Test',
                                                 'run_Mealy.test_file_decode'))
    try:
        os.remove(pathTestFileResult)
        os.remove(pathTestFileDecode)
    except FileNotFoundError:
        pass

    # Cypher pathTestFile
    progName = "run_Mealy.py"
    numKey = "123"
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-n ' + numKey,
                  '-i ' + pathTestFile, '-o ' + pathTestFileResult])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileResult)

    # Reverse operation
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-d', '-n ' + numKey,
                  '-i ' + pathTestFileResult, '-o ' + pathTestFileDecode])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileDecode)

    # Diff origin / decoded file to check if they match
    with open(pathTestFile) as f1, open(pathTestFileDecode) as f2:
        f1_text = f1.read()
        f2_text = f2.read()
        assert not list(difflib.unified_diff(f1_text, f2_text,
                                         fromfile=pathTestFile,
                                         tofile=pathTestFileDecode,
                                         lineterm=''))

@pytest.mark.parametrize( "verbose", [True, False])
def test_batch_cypher_decypher_simple_string(verbose):
    """ Simple batch ciphering / decyphering """

    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    pathTest = config.get('Test', 'run_Mealy.path_test')
    print("pathOutput directory =", pathTest)

    # Check test environment
    assert os.path.isdir(pathTest), f"First create {pathTest} dir !"
    inputText = config.get('Test', 'run_Mealy.inputText')
    assert inputText, "input text must contain text"
    pathTestFileResult = os.path.join(pathTest,
                                      config.get('Test',
                                                 'run_Mealy.test_string_result'))
    pathTestFileDecode = os.path.join(pathTest,
                                      config.get('Test',
                                                 'run_Mealy.test_string_decode'))
    try:
        os.remove(pathTestFileResult)
        os.remove(pathTestFileDecode)
    except FileNotFoundError:
        pass

    # Cypher inputText
    progName = "run_Mealy.py"
    numKey = "123"
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-n ' + numKey,
                  '-t ' + inputText, '-o ' + pathTestFileResult])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileResult)

    # Reverse operation
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-d', '-n ' + numKey,
                  '-i ' + pathTestFileResult, '-o ' + pathTestFileDecode])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileDecode)

    # Diff origin / decoded file to check if they match
    with open(pathTestFileDecode) as f2:
        f1_text = inputText
        f2_text = f2.read()
        assert not list(difflib.unified_diff(f1_text, f2_text,
                                         fromfile="inputText",
                                         tofile=pathTestFileDecode,
                                         lineterm=''))

@pytest.mark.parametrize( "verbose", [True, False])
def test_batch_cypher_decypher_2keys_string(verbose):
    """ Batch ciphering / decyphering with key + strings """

    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    pathTest = config.get('Test', 'run_Mealy.path_test')
    print("pathOutput directory =", pathTest)

    # Check test environment
    assert os.path.isdir(pathTest), f"First create {pathTest} dir !"
    pathTestFile = os.path.join(pathTest,
                                config.get('Test', 'run_Mealy.test_file'))
    assert os.path.isfile(pathTestFile), f"{pathTestFile} must exist"
    pathTestFileResult = os.path.join(pathTest,
                                      config.get('Test',
                                                 'run_Mealy.test_file_result'))
    pathTestFileDecode = os.path.join(pathTest,
                                      config.get('Test',
                                                 'run_Mealy.test_file_decode'))
    stringkeys = [config.get('Test', 'run_Mealy.test_key_string' + num)
                  for num in ["1", "2"]]
    pathTestFileResult2k = [os.path.join(pathTest, stringKey + '_' +
                                                  config.get('Test',
                                 'run_Mealy.test_file_result_2k'))
                            for stringKey in stringkeys]
    pathTestFileDecode2k = [os.path.join(pathTest, stringKey + '_' +
                                                  config.get('Test',
                                 'run_Mealy.test_file_decode'))
                            for stringKey in stringkeys]

    try:
        os.remove(pathTestFileResult)
        os.remove(pathTestFileDecode)
        for pathFile in pathTestFileResult2k:
            os.remove(pathFile)
        for pathFile in pathTestFileDecode2k:
            os.remove(pathFile)
    except FileNotFoundError:
        pass

    progName = "run_Mealy.py"
    numKey = "123"

    # Cypher text with two additionnal different keys
    for num, stringKey in enumerate(stringkeys):
        # Cypher pathTestFile with key
        param = [progName]
        if verbose:
            param.extend(['-v'])
        param.extend(['-b', '-n ' + numKey, '-s ' + stringKey,
                  '-i ' + pathTestFile, '-o ' + pathTestFileResult2k[num]])
        print(param)
        assert run_Mealy.main(param) == 0
        assert os.path.isfile(pathTestFileResult2k[num])

        # Reverse operation
        param = [progName]
        if verbose:
            param.extend(['-v'])
        param.extend(['-b', '-d', '-n ' + numKey, '-s ' + stringKey,
                  '-i ' + pathTestFileResult2k[num],
                  '-o ' + pathTestFileDecode2k[num]])
        print(param)
        assert run_Mealy.main(param) == 0
        assert os.path.isfile(pathTestFileDecode2k[num])

        # Diff origin /decoded file to check if they match
        with open(pathTestFile) as f1,\
             open(pathTestFileDecode2k[num]) as f2:
            f1_text = f1.read()
            f2_text = f2.read()
            assert not list(difflib.unified_diff(f1_text, f2_text,
                                         fromfile=pathTestFile,
                                         tofile=pathTestFileDecode2k[num],
                                         lineterm=''))

    # Cypher pathTestFile
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-n ' + numKey,
                  '-i ' + pathTestFile, '-o ' + pathTestFileResult])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileResult)

    # Test if cyphered versions are different for 3 encoded texts
    for num in range(1):
        with open(pathTestFile) as f1,\
            open(pathTestFileResult2k[num]) as f2:
            f1_text = f1.read()
            f2_text = f2.read()
            assert list(difflib.unified_diff(f1_text, f2_text,
                                         fromfile=pathTestFile,
                                         tofile=pathTestFileResult2k[num],
                                         lineterm=''))

        with open(pathTestFileResult2k[0]) as f1,\
            open(pathTestFileResult2k[1]) as f2:
            f1_text = f1.read()
            f2_text = f2.read()
            assert list(difflib.unified_diff(f1_text, f2_text,
                                         fromfile=pathTestFileResult2k[0],
                                         tofile=pathTestFileResult2k[1],
                                         lineterm=''))

@pytest.mark.parametrize( "verbose", [True, False])
def test_batch_cypher_decypher_2keys_file(verbose):
    """ batch ciphering / decyphering key + 2nd key in file"""

    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    pathTest = config.get('Test', 'run_Mealy.path_test')
    print("pathOutput directory =", pathTest)

    # Check test environment
    assert os.path.isdir(pathTest), f"First create {pathTest} dir !"
    pathTestFile = os.path.join(pathTest,
                                config.get('Test', 'run_Mealy.test_file'))
    assert os.path.isfile(pathTestFile), f"{pathTestFile} must exist"

    stringKey = config.get('Test', 'run_Mealy.test_key_string1')
    pathTestFileResultString = os.path.join(pathTest, stringKey + '_string_' +
                    config.get('Test', 'run_Mealy.test_filekey_result'))
    pathTestFileResultFile = os.path.join(pathTest, stringKey + '_file_' +
                    config.get('Test', 'run_Mealy.test_filekey_result'))
    pathFileKey = os.path.join(pathTest,
                               config.get('Test', 'run_Mealy.test_filekey'))
    try:
        os.remove(pathTestFileResultString)
        os.remove(pathTestFileResultFile)
        os.remove(pathFileKey)
    except FileNotFoundError:
        pass

    progName = "run_Mealy.py"
    numKey = "123"

    # Cypher with key and string
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-n ' + numKey, '-s ' + stringKey,
                  '-i ' + pathTestFile, '-o ' + pathTestFileResultString])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileResultString)

    # Cypher with key and file containing string
    with open(pathFileKey, "w") as hKey:
        hKey.write(stringKey)
    param = [progName]
    if verbose:
        param.extend(['-v'])
    param.extend(['-b', '-n ' + numKey, '-f ' + pathFileKey,
                  '-i ' + pathTestFile, '-o ' + pathTestFileResultFile])
    print(param)
    assert run_Mealy.main(param) == 0
    assert os.path.isfile(pathTestFileResultFile)

    # Diff to cyphered files to check if they match
    with open(pathTestFileResultString) as f1,\
             open(pathTestFileResultFile) as f2:
        f1_text = f1.read()
        f2_text = f2.read()
        assert not list(difflib.unified_diff(f1_text, f2_text,
                                         fromfile=pathTestFileResultString,
                                         tofile=pathTestFileResultFile,
                                         lineterm=''))
