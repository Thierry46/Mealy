#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
*********************************************************
Class : MealyGUI
Auteur : Thierry Maillard (TM)
Date : 7/5/2015 - 1/2/2021

Rôle : GUI for Mealy ciphering machine.

Licence : GPLv3
Copyright (c) 2021 - Thierry Maillard


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

Modifications :
V3.0 : Support python 3
*********************************************************
"""

import importlib # To test if module are available

import tkinter
import gettext

import CardFrame
import KeysFrame
import CypherFrame
import ResultFrame


class MealyGUI(tkinter.Tk):
    """
    A GUI for Mealy ciphering machine.
    """
    def __init__(self, master, config, verbose):
        """
        Constructor
        Define all GUIs widgets
        parameters :
            - master : its parent
            - config : configuration properties read by ConfigParser
            - verbose : true if debug information are displayed
        """
        tkinter.Tk.__init__(self, master)
        self.verbose = verbose
        self.config = config

        if self.verbose :
            print("Enter in MealyGUI constructor")

        self.title(f"{self.config.get('Version', 'appName')} - "
                   f"{self.config.get('Version', 'number')} - "
                   f"{self.config.get('Version', 'date')}")

        self.setStateSteganography()

        # Build Card frames and its action button in mainFrame
        mainFrame = tkinter.Frame(self)
        cardFrame = CardFrame.CardFrame(mainFrame, self.verbose)

        # Add frames in cardFrame
        keyFrames = KeysFrame.KeysFrame(cardFrame,
                            self,
                            _('Mealy - Enter keys'),
                            self.verbose)
        cardFrame.addFrame(keyFrames)
        cipherFrame = CypherFrame.CipherFrame(cardFrame,
                            self,
                            _('Mealy - Cipher / Decipher'),
                            self.verbose)
        cardFrame.addFrame(cipherFrame)
        resultFrame = ResultFrame.ResultFrame(cardFrame,
                            self,
                            _('Mealy - Results'),
                            self.verbose)
        cardFrame.addFrame(resultFrame)
        cardFrame.displayFirstFrame()

        # Status line
        statusFrame = tkinter.LabelFrame(self, text=_("Messages"))
        self.messageLabel = tkinter.Label(statusFrame, text=_("Ready !"))
        self.messageLabel.pack(side = tkinter.LEFT)
        statusFrame.pack(side = tkinter.BOTTOM, fill="both", expand="yes")
        mainFrame.pack()

        if self.verbose :
            print("Exit from MealyGUI constructor")

    def setMessageLabel(self, text, error=False):
        """ Display a message to user at the bottom of the frame """
        self.messageLabel['text'] = text
        if error:
            self.bell()

    def setStateSteganography(self):
        """ Test if steganography module are installed """
        specPIL = importlib.util.find_spec('PIL')
        specStepic = importlib.util.find_spec('stepic')
        if specPIL and specStepic:
            print("Steganography available : PIL and stepic module found.")
            self.stateSteganography = tkinter.NORMAL
        else:
            print("Warning : Feature steganography not avalailable !")
            print("To make it is available,",
                  "download and install Python these modules with pip :")
            print("\tPIL  doc : https://pypi.org/project/Pillow")
            print("\tstepic doc : https://pypi.org/project/stepic")
            self.stateSteganography = tkinter.DISABLED

def runGUI(verbose, nbState) :
    """
    verbose : True if debug messages are displayed.
    nbState : Number aof state in Mealy transition table
    """
    if verbose :
        print(f"Enter in LaunchGUI(verbose={verbose}, nbState={nbState})")

    app = MealyGUI(None, nbState, verbose)
    app.mainloop()

    if verbose :
        print("Exit from LaunchGUI")
