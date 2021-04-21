# -*- coding: utf-8 -*-
"""
*********************************************************
Class : steganography.py
Author: Thierry Maillard (TMD)
Date: 12/3/2021 - 22/3/2021

Role: Steganograhy : hide or extract a text in an image

Licence: GPLv3
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
*********************************************************
"""

from PIL import Image
import stepic

def hideTextInImage(fileNameInput, fileNameOutput, textToWrite, verbose):
    """
    Hide a text in an image that is read and written on disk.
    return : 0 if ok, 1 if problem with fileNameInput,
             2 if problem with fileNameOutput,
             3 if io problem

    parameters :
    - fileNameInput : path of the original file
    - fileNameOutput : path name of output file with text hidden inside
    - textToWrite : text string to hide in file
    - verbose : True if message can be written on stdout file
    """

    cr = 0

    if verbose :
        print("Enter in hideTextinImage()")
        print("fileNameInput=", fileNameInput)
        print("fileNameOutput=", fileNameOutput)
        print("textToWrite=", textToWrite)

    try:
        if fileNameInput:
            image = Image.open(fileNameInput)
            formatImage = image.format

            # v3.0 : stepic.encode_inplace should be an array of int
            dataIntArray = [ord(char) for char in textToWrite]
            print("image.mode", image.mode)
            stepic.encode_inplace(image, dataIntArray)

            if fileNameOutput:
                image.save(fileNameOutput, formatImage)
            else:
                cr = 2
        else:
            cr = 1
    except IOError as exc:
        print("exception =", exc)
        cr = 3

    if verbose :
        print("Exit from hideTextinImage(), cr=", cr)

    return cr

def extractTextFromImage(fileNameInput, verbose):
    """
    Extract text hidden in an image.
    return :
            cr : 0 if ok, 1 if problem with fileNameInput,
                 2 if io problem
            resultText : text extracted from image

    parameters :
    - fileNameInput : path of the image file
    - resultText : text string extracted from image
    - verbose : True if message can be written on stdout file
    """

    cr = 0
    resultText = None

    if verbose :
        print("Enter in extractTextFromImage()")
        print("fileNameInput=", fileNameInput)

    try:
        if fileNameInput:
            image = Image.open(fileNameInput)
            resultText = stepic.decode(image)
        else:
            cr = 1
    except IOError as exc:
        print("exception =", exc)
        cr = 2

    if verbose :
        print("Exit from extractTextFromImage(), cr=", cr,
              "resultText=", resultText)

    return cr, resultText
