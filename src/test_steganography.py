# coding: utf-8
"""
Name : test_steganography
Author : Thierry Maillard (TMD)
Date : 23/3/2021
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

import steganography

@pytest.mark.parametrize( "text", ["Salut tout le monde !",
                                   "é&èçà",
                                   "0123456789" +
                        "abcdefghijklmnopqrstuvwxyz" +
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n"+
                        "àãáâÀÃÁÂéèêëÉÈÊËîïÎÏùüûÙÜÛôöÔÖçÇ«»"])
def test_steganography_ok(text):
    """
    Steganography test : hide a text in an image and
    test reverse operation
    """

    config = configparser.RawConfigParser()
    config.read('Mealy.ini')

    pathTest = config.get('Test', 'run_Mealy.path_test')
    print("pathOutput directory =", pathTest)

    # Check test environment
    assert os.path.isdir(pathTest), f"First create {pathTest} dir !"
    pathTestImage = os.path.join(pathTest,
                                config.get('Test', 'steganography.image'))
    assert os.path.isfile(pathTestImage), f"{pathTestImage} must exist"
    pathTestImageResult = os.path.join(pathTest,
                                      config.get('Test',
                                                 'steganography.imageResult'))
    try:
        os.remove(pathTestImageResult)
    except FileNotFoundError:
        pass

    # Hide text in image
    cr = steganography.hideTextInImage(pathTestImage, pathTestImageResult,
                                       text, True)
    assert cr == 0

    # Extract text from image
    cr, textResult = steganography.extractTextFromImage(pathTestImageResult,
                                                        True)
    assert cr == 0
    assert textResult == text
