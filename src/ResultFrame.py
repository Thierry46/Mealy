# -*- coding: utf-8 -*-
"""
*********************************************************
Class  : ResultFrame.py
Author : Thierry Maillard (TMD)
Date : 22/5/2015 - 1/4/2021

Role : Frame used to display cyphering results

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
import os
import os.path

import tkinter
import tkinter.filedialog
import gettext

import CardFrame

class ResultFrame(CardFrame.CardFrameChild):
    """ Frame used to display cyphering results """

    def __init__(self, master, root, name, verbose=False):
        """
        Constructor : build widgets for cyphering results
        Parameters :
            - master : its parent
            - root : application GUI root
            - name to be displayed in this frame's border
            - verbose : true if debug information are displayed
        """
        CardFrame.CardFrameChild.__init__(self, master,
                root, name, verbose)
        self.pack(side=tkinter.TOP, padx=10, pady=10)

        tkinter.Label(self, text=_("Text processed")).grid(row=0, column=0)

        self.resultTextEditor = tkinter.Text(self,
                wrap=tkinter.NONE,
                height=5, width=60, background = 'YELLOW',
               )
        self.resultTextEditor.grid(row=1, columnspan=2)
        scrollbarRight = tkinter.Scrollbar(self,
                                           command=self.resultTextEditor.yview)
        scrollbarRight.grid(row=1, column=2, sticky='wns')
        scrollbarBottom = tkinter.Scrollbar(self,
                                            orient=tkinter.HORIZONTAL,
                                            command=self.resultTextEditor.xview)
        scrollbarBottom.grid(row=2, columnspan=2, sticky='new')
        self.resultTextEditor.config(yscrollcommand=scrollbarRight.set)
        self.resultTextEditor.config(xscrollcommand=scrollbarBottom.set)

        tkinter.Label(self,
                text=_("Save in a file :")
                ).grid(row=4, column=0, sticky='e')
        tkinter.Button(self,
            text=_(".txt..."),
            command=self.saveTxtButtonCallback
            ).grid(row=4, column=1)
        tkinter.Button(self,
            text=_(".png..."),
            command=self.savePngButtonCallback,
            state=self.root.stateSteganography
            ).grid(row=4, column=3)

        # Don't display this frame now
        self.pack_forget()

    ################
    # Callbacks
    ################
    def saveTxtButtonCallback(self) :
        """
        Callback for button that launch file chooser to save results.
        if a file is selected, save result text editor in it.
        V3.0 : encoding = utf8 + context manager (with)
        """
        if self.verbose :
            print("Enter in saveTxtButtonCallback()")

        try :
            fileName = tkinter.filedialog.asksaveasfilename(
                        title=_("Select a filename for saving result"),
                        defaultextension='.txt')
            if fileName != "":
                with open(fileName, 'w', encoding='utf8') as outfile:
                    # 'end-1c' to remove last newline added by Tkinter Text component
                    textToWrite = self.resultTextEditor.get('1.0', 'end-1c')
                    outfile.write(textToWrite)
                    self.root.setMessageLabel(_('Results saved in file') + ' : ' + \
                                              os.path.basename(fileName))
            else :
                self.root.setMessageLabel(_('Results not saved !'))

        except IOError as exc:
            self.bell()
            self.root.setMessageLabel(_('Unable to save results in file') + \
                ' : ' + os.path.basename(fileName))
            print(f'Unable to save results in file : {fileName} : \n\t{exc}')

        if self.verbose :
            print("Exit from saveTxtButtonCallback()")

    def savePngButtonCallback(self):
        """
        Callback for button that launch file chooser to save and hide results in an image.
        if a file is selected, save result text editor in it.
        Only called if steganography is available.
        """
        import steganography

        if self.verbose:
            print("Enter in savePngButtonCallback()")

        fileName = tkinter.filedialog.askopenfilename(
                    filetypes=[("All", "*"),("PNG image","*.png")],
                    title=_("Select a PNG file to hide text in it (read only)"))
        # 'end-1c' to remove last newline added by Tkinter Text component
        textToWrite = self.resultTextEditor.get('1.0', 'end-1c')

        image_out = tkinter.filedialog.asksaveasfilename(
                    filetypes = [("PNG image","*.png"),],
                    title=_("Select a filename for saving result"),
                    defaultextension='.png')

        cr = steganography.hideTextInImage(fileName, image_out,
                                           textToWrite, self.verbose)
        if cr == 0:
            self.root.setMessageLabel(_('Results saved in file') + ' : ' + \
                    os.path.basename(image_out))
        elif cr==2:
            self.root.setMessageLabel(_('Results not saved !'))
        elif cr==1:
            self.root.setMessageLabel(_('Results not saved !'))
        else:
            self.root.setMessageLabel(_('Unable to save results in file') + \
                                      ' : ' + os.path.basename(fileName),
                                      True)

        if self.verbose:
            print("Exit from savePngButtonCallback()")

    ##################
    # Init Function
    # Override class CardFrameChild/todoWhenDisplayed(self)
    ##################
    def todoWhenDisplayed(self):
        if self.verbose :
            print("Enter in ResultFrame/todoWhenDisplayed()")

        self.resultTextEditor.delete('1.0', tkinter.END)
        self.resultTextEditor.insert(tkinter.INSERT, self.root.resultText)

        if self.verbose :
            print("Exit from ResultFrame/todoWhenDisplayed()")
