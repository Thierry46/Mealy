# -*- coding: utf-8 -*-
"""
*********************************************************
Class  : KeysFrame.py
Author : Thierry Maillard (TMD)
Date : 22/5/2015 - 25/2/2021

Role : Frame used to enter keys for Mealy Machine

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

Modifications :
*********************************************************
"""

 # To print on stderr
import tkinter
import tkinter.filedialog
import gettext

import CardFrame
import Mealy


class KeysFrame(CardFrame.CardFrameChild):
    """ Frame used to enter keys for Mealy Machine """
    def __init__(self, master, root, name, verbose=False):
        """
        Constructor : build widgets to enter keys
        Parameters :
            - master : its parent
            - root : application GUI root
            - name to be displayed in this frame's border
            - verbose : true if debug information are displayed
        """
        CardFrame.CardFrameChild.__init__(self, master,
                root, name, verbose)
        self.pack(side=tkinter.TOP, padx=10, pady=10)

        tkinter.Label(self, text=_("Numeric key :")).grid(row=0, column=0,
                                                          sticky=tkinter.W)
        self.numericKey = tkinter.StringVar()
        self.keyValueEntry = tkinter.Entry(self, textvariable=self.numericKey)
        self.keyValueEntry.grid(row=0, column=1, columnspan=2,
                                sticky=tkinter.W)
        self.extFileCheckVar = tkinter.IntVar()
        self.extKeyCheckbutton = tkinter.Checkbutton(self,
            text=_("With character key (for security)"),
            variable=self.extFileCheckVar,
            command=self.extKeyButtonCallback)
        self.extKeyCheckbutton.grid(row=1, columnspan=3, sticky=tkinter.W)

        ##################
        # Char key buttons
        ##################
        self.varRadiobuttonSource = tkinter.IntVar()
        self.varRadiobuttonSource.set(0)

        self.kbInputbutton = tkinter.Radiobutton(self,
                    text=_("Keyboard input :"),
                    variable=self.varRadiobuttonSource,
                    value=0, state=tkinter.DISABLED,
                    command=self.extKeyButtonCallback
                    )
        self.kbInputbutton.grid(row=3, column=0, sticky=tkinter.W)

        self.localFileRadiobutton = tkinter.Radiobutton(self,
                    text=_("Local file :"),
                    variable=self.varRadiobuttonSource,
                    value=1, state=tkinter.DISABLED,
                    command=self.extKeyButtonCallback)
        self.localFileRadiobutton.grid(row=3, column=1, sticky=tkinter.E)
        self.filechooserLocalFileButton = tkinter.Button(self,
            text="...", state=tkinter.DISABLED,
            command=self.fileChooserKeybuttonCallback
            )
        self.filechooserLocalFileButton.grid(row=3, column=3, sticky=tkinter.W)

        self.sourceKeyPageName = tkinter.StringVar()
        self.keyFileNameEntry = tkinter.Entry(self,
              textvariable=self.sourceKeyPageName,
              state=tkinter.DISABLED)
        self.keyFileNameEntry.grid(row=4, column=0, columnspan=5, sticky=tkinter.EW)

        # Don't display this frame now
        self.pack_forget()

    ################
    # Callbacks
    ################
    def fileChooserKeybuttonCallback(self) :
        """
        Callback for button that
        Display a file chooser for key file and
        if a file is selected, display its name in entry.
        """
        if self.verbose :
            print("Enter in fileChooserKeybuttonCallback()")

        fileName = tkinter.filedialog.askopenfilename(
                        title=_("Select a file containing additional key"))
        if fileName != "" :
            self.sourceKeyPageName.set(fileName)

        if self.verbose :
            print("Exit from fileChooserKeybuttonCallback()")

    def extKeyButtonCallback(self) :
        """
        Active or disactive all controls in externalKeyFileWindow
        parameter :
            stateFlag : NORMAL or DISABLED
        """
        if self.verbose :
            print("Enter in setStateKeyInput()")

        if self.extFileCheckVar.get() == 0 :
            stateFlag = tkinter.DISABLED
        else :
            stateFlag = tkinter.NORMAL

        if self.verbose :
            print("State set to " + stateFlag)

        self.kbInputbutton.configure(state=stateFlag)
        self.localFileRadiobutton.configure(state=stateFlag)
        self.keyFileNameEntry.configure(state=stateFlag)

        # Activate File chooser buton only if presse button is local file
        numPressedButton = self.varRadiobuttonSource.get()
        if self.verbose :
            print("numPressedButton ="+str(numPressedButton))

        if numPressedButton == 1 and stateFlag == tkinter.NORMAL :
            self.filechooserLocalFileButton.configure(state=tkinter.NORMAL)
        else :
            self.filechooserLocalFileButton.configure(state=tkinter.DISABLED)

        if self.verbose :
            print("Exit from setStateKeyInput()")

    ##############################################
    # Validation before going to next frame
    # Override class CardFrameChild/validate(self)
    ##############################################
    def validate(self) :
        """
        Callback for button validateKeyButton.
        If keys values are ok, create mealy machine.
        """
        if self.verbose :
            print("Enter in KeysFrame/validate()")

        error = False
        try :
            key = int(self.numericKey.get())
            if key < 0 :
                raise ValueError(_("Key must be a positive integer !"))
            if self.extFileCheckVar.get() == 0 :
                typeEntity = 'printable'
                file = ''
            else :
                possibleType = ['string', 'file']
                numPressedButton = self.varRadiobuttonSource.get()
                typeEntity = possibleType[numPressedButton]
                file = self.sourceKeyPageName.get()

            if self.verbose :
                print('Starting Mealy machine :')
                print('With parameters : key=' + str(key) +
                    ',typeEntity=' + typeEntity +
                    ',file=' + file)

            mealy = Mealy.Mealy(key, self.root.config, typeEntity, file, self.verbose)
            mealy.genAlphabetMatrixes()
            if not mealy.isReady() :
                raise ValueError(_("Mealy machine not ready !"))
            self.root.mealy = mealy
            self.root.setMessageLabel(_('Mealy machine started : Ready'))
            if self.verbose :
                print('Mealy machine started : Ready')

        except ValueError as exc:
            self.bell()
            self.root.setMessageLabel(_("Problem : ") + str(exc))
            error = True

        returnValue = not error
        if self.verbose :
            print("Exit from KeysFrame/validate(), OK= " + str(returnValue))

        return returnValue
