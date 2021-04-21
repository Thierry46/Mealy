# -*- coding: utf-8 -*-
"""
*********************************************************
Class : CipherFrame.py
Author: Thierry Maillard (TMD)
Date: 22/5/2015 - 25/2/2021

Role: Frame used to set cyphering parameters

Licence: GPLv3
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

 # To print on stderr
import os
import os.path
import sys
import string

import tkinter
import tkinter.filedialog
import gettext

import CardFrame


class CipherFrame(CardFrame.CardFrameChild):
    """ Frame for cyphering imput parameters """
    def __init__(self, master, root, name, verbose=False):
        """
        Constructor: build widgets for cyphering parameters
        Parameters:
            - master: its parent
            - root: application GUI root
            - name to be displayed in this frame's border
            - verbose: true if debug information are displayed
        """
        CardFrame.CardFrameChild.__init__(self, master,
                                          root, name, verbose)
        self.pack(side=tkinter.TOP, padx=10, pady=10)

        self.varRadiobuttonAction = tkinter.IntVar()
        self.varRadiobuttonAction.set(1)
        tkinter.Radiobutton(self,
                            text=_("Cipher"),
                            variable=self.varRadiobuttonAction,
                            value=1,
                            ).grid(row=0, column=0)
        tkinter.Radiobutton(self,
                            text=_("Decipher"),
                            variable=self.varRadiobuttonAction,
                            value=2,
                            ).grid(row=0, column=1)

        tkinter.Label(self,
                      text=_("Or type your text in editor below:")
                      ).grid(row=1, column=0, columnspan=2)

        self.textEditor = tkinter.Text(self,
                                       wrap=tkinter.NONE,
                                       height=5, width=60,
                                       background = 'ORANGE',
               )
        self.textEditor.grid(row=2, column=0, columnspan=4, sticky='ew')
        scrollbarRight = tkinter.Scrollbar(self, command=self.textEditor.yview)
        scrollbarRight.grid(row=2, column=4, sticky='wns')
        scrollbarBottom = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL,
                                            command=self.textEditor.xview)
        scrollbarBottom.grid(row=3, columnspan=4, sticky='new')
        self.textEditor.config(yscrollcommand=scrollbarRight.set)
        self.textEditor.config(xscrollcommand=scrollbarBottom.set)

        tkinter.Button(self,
                       text=_("Clear"),
                       command=self.clearTextButtonCallback
                       ).grid(row=4, column=0, sticky='w')

        tkinter.Label(self,
                      text=_("Insert from:")
                     ).grid(row=4, column=1, sticky='e')
        tkinter.Button(self,
                       text=_(".txt file..."),
                       command=self.fileChooserTextFileButtonCallback
                      ).grid(row=4, column=2)

        tkinter.Button(self,
                       text=_(".png file..."),
                       command=self.fileChooserImageButtonCallback,
                       state=self.root.stateSteganography
                      ).grid(row=4, column=3)

        # Don't display this frame now
        self.pack_forget()

    ################
    # Callbacks
    ################
    def clearTextButtonCallback(self):
        """
        Callback for clear button: erase text editor.
        """
        if self.verbose:
            print("Enter in clearTextButtonCallback()")

        self.textEditor.delete('1.0', tkinter.END)

        if self.verbose:
            print("Exit from clearTextButtonCallback()")

    def fileChooserTextFileButtonCallback(self):
        """
        Callback for button that launch file chooser for text.
        Display a file chooser for text file and
        if a file is selected, insert it into text editor.
        V3.0: encoding = utf8 + context manager (with)
        """
        if self.verbose:
            print("Enter in fileChooserTextFileButtonCallback()")

        try:
            fileName = tkinter.filedialog.askopenfilename(
                        title=_("Select a file containing text to insert"))
            if fileName != "":
                with open(fileName, 'r', encoding='utf8') as infile:
                    self.textEditor.insert(tkinter.INSERT, infile.read())
                    self.root.setMessageLabel(_('Text inserted from: ') +
                                              os.path.basename(fileName))
        except IOError:
            self.root.setMessageLabel(_('Unable to read text file !'))

        if self.verbose:
            print("Exit from fileChooserTextFileButtonCallback()")

    def fileChooserImageButtonCallback(self):
        """
        Callback for button that launch file chooser for Image.
        Display a file chooser for image file and
        if a file is selected, extract text hidden in it with stepic module
        insert text into text editor.
        Only called if steganography is available.
        """

        from PIL import Image # pylint: disable=import-outside-toplevel
        import stepic # pylint: disable=import-outside-toplevel

        if self.verbose:
            print("Enter in fileChooserImageButtonCallback()")

        try:
            fileName = tkinter.filedialog.askopenfilename(
                        filetypes = (("All", "*"),("PNG Image","*.png")),
                        title=_("Select a file containing text to insert"))
            if fileName != "":
                image = Image.open(fileName)
                text = stepic.decode(image)
                if self.verbose:
                    print("Text read from " + fileName + ": " + text)
                self.textEditor.insert(tkinter.INSERT, text)
                self.root.setMessageLabel(_("Text read from ") +
                                          os.path.basename(fileName))

        except IOError:
            self.root.setMessageLabel(_('Unable to read text file !') + ': ' +
                                         + os.path.basename(fileName))

        if self.verbose:
            print("Exit from fileChooserImageButtonCallback()")


    ##############################################
    # Validation before going to next frame
    # Override class CardFrameChild/validate(self)
    ##############################################
    def validate(self):
        """
        Callback for button validateKeyButton.
        If keys values are ok, create mealy machine.
        """
        if self.verbose:
            print("Enter in CypherFrame/validate()")

        error = False

        cipher = (self.varRadiobuttonAction.get() == 1)
        # 'end-1c' to remove last newline added by Tkinter Text component
        textToProcess = self.textEditor.get('1.0', 'end-1c')

        emptyEditor = (len(textToProcess) <= 0)

        if self.verbose:
            print(f"textToProcess={textToProcess}")
            print(f"emptyEditor={emptyEditor}, cipher={cipher}")

        if not emptyEditor:
            try:
                if cipher:
                    resultText = self.root.mealy.cipher(textToProcess)
                else:
                    resultText = self.root.mealy.deCipher(textToProcess)
                self.root.setMessageLabel(_("Message processed : OK"))
                self.root.resultText = resultText
            except ValueError as exc:
                error = True
                self.bell()
                print('Mealy error when processing text :', file=sys.stderr)
                print(exc, file=sys.stderr)
                self.root.setMessageLabel(_("Problem when processing text !"))
        else:
            error = True
            self.bell()
            self.root.setMessageLabel(_("Please enter a text !"))

        returnValue = not error
        if self.verbose:
            print(f"Exit from CypherFrame/validate(), OK= {returnValue}")

        return returnValue
