# -*- coding: utf-8 -*-
"""
*********************************************************
Class  : CardFrame.py
Author : Thierry Maillard (TMD)
Date : 13/5/2015

Role : CardFrame layout.
    A container where inside frame are stacked
    Provide 2 buttons prev, next to change the inside frame displayed

Modifications :

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

import tkinter
import gettext


class CardFrame(tkinter.Frame):
    """
    A container where inside frame (CardFrameChild) are stacked
    Provide 2 buttons prev, next to change the inside frame displayed
    """
    def __init__(self, master, verbose):
        """
        Constructor : build 2 subframes :
            - One for stacked frame
            - One for commands buttons
        Parameters ;
            - master : owner of this frame (above frame)
        """
        tkinter.Frame.__init__(self, master)
        self.listFrame = []
        self.currentFrame = 0
        self.verbose = verbose

        if self.verbose :
            print("Enter in CardFrame constructor")

        # Create a subframe for buttons back and next
        # at the bottom of master frame
        ButtonsFrame = tkinter.Frame(master)
        ButtonsFrame.pack(side = tkinter.BOTTOM, padx=10)
        self.backButton = tkinter.Button(ButtonsFrame,
            text=_("Go back..."),
            command=self.displayPreviousFrame)
        self.backButton.grid()
        #row=0, column=0, sticky=W
        self.nextButton = tkinter.Button(ButtonsFrame,
            text=_("Go next..."),
            command=self.displayNextFrame)
        self.nextButton.grid()
        self.backButton.grid_forget()
        self.nextButton.grid_forget()

        if self.verbose :
            print("Exit of CardFrame constructor")

    def addFrame(self, frame):
        """ Add a frame at the end of the list of frames """
        if self.verbose :
            print("Enter in addFrame()")
        self.listFrame.append(frame)
        if self.verbose :
            print("Exit of addFrame()")

    def displayFirstFrame(self):
        """ Display first frame """
        if self.verbose :
            print("Enter in displayFirstFrame()")
        self.displayFrame(0)
        if self.verbose :
            print("Exit of displayFirstFrame()")

    def displayPreviousFrame(self):
        """ display Previous Frame """
        if self.verbose :
            print("Enter in displayPreviousFrame()")
        self.displayFrame(self.currentFrame - 1)
        if self.verbose :
            print("Exit of displayPreviousFrame()")

    def displayNextFrame(self):
        """ displayNextFrame """
        if self.verbose :
            print("Enter in displayNextFrame()")
        self.displayFrame(self.currentFrame + 1)
        if self.verbose :
            print("Exit of displayNextFrame()")

    def isFirstFrame(self):
        """ Return True if first frame is displayed """
        if self.verbose :
            print("Enter in isFirstFrame()")
        if len(self.listFrame) == 0 :
            raise ValueError('Empty card frame')
        returnValue = (self.currentFrame == 0)
        if self.verbose :
            print("Exit of isFirstFrame(), return " + str(returnValue))
        return returnValue

    def isLastFrame(self):
        """ Return True if last frame is displayed """
        if self.verbose :
            print("Enter in isLastFrame()")
        if len(self.listFrame) == 0 :
            raise ValueError('Empty card frame')
        returnValue = (self.currentFrame >= len(self.listFrame) - 1)
        if self.verbose :
            print("Exit of isLastFrame(), return " + str(returnValue))
        return returnValue

    def isValidNumFrame(self, numFrame):
        """
        Return True if numFrame is the number of a frame that exists.
        Throw ValueError exception if there is no frame registred
        """
        if self.verbose :
            print("Enter in isValidNumFrame()")
        if len(self.listFrame) == 0 :
            raise ValueError('Empty card frame')
        returnValue = (0 <= numFrame < len(self.listFrame))
        if self.verbose :
            print("Exit of isValidNumFrame(), return " + str(returnValue))
        return returnValue

    def displayFrame(self, numFrame):
        """
        Display a frame wich number is given by user.
        Throw ValueError exception if there is no frame registred
        """
        if self.verbose :
            print("Enter in displayFrame()")
            print("numFrame = " + str(numFrame))
            print("self.currentFrame = " + str(self.currentFrame))

        # If frame change is allowed, hide old one
        # Validation only if frame number is growing
        if self.isValidNumFrame(numFrame):
            if numFrame > self.currentFrame :
                if self.listFrame[self.currentFrame].validate():
                    self.listFrame[self.currentFrame].pack_forget()
                    self.currentFrame = numFrame
            else: # No control with validate() when returning to previous frame
                self.listFrame[self.currentFrame].pack_forget()
                self.currentFrame = numFrame

        # Display the begining or new frame on the top of the heap
        if numFrame == self.currentFrame:
            self.listFrame[self.currentFrame].todoWhenDisplayed()
            self.listFrame[self.currentFrame].pack()

        # Display or hide commands button according
        if self.isFirstFrame():
            self.backButton.grid_forget()
        else:
            self.backButton.grid()
        if self.isLastFrame():
            self.nextButton.grid_forget()
        else:
            self.nextButton.grid()
        self.pack()

        if self.verbose :
            print("Exit of displayFrame()")
            print("with self.currentFrame = " + str(self.currentFrame))

class CardFrameChild(tkinter.LabelFrame):
    """ A frame that can be dealed by CardFrame """
    def __init__(self, master, root, name, verbose):
        """
        Constructor : for a frame
        Parameters :
            - master : its parent
            - root : application GUI root
            - name to be displayed in this frame's border
            - verbose : true if debug information are displayed
            with a validation methode
        """
        tkinter.LabelFrame.__init__(self, master, text=name)
        self.root = root
        self.verbose = verbose

    def validate(self):
        """
        Abstract methode that subclass must implement
        Implementation must return True of OK, False else
        """
        raise Exception("NotImplementedException")

    def todoWhenDisplayed(self):
        """
        Empty method for initialisation when entering in a frame
        must be overloaded if necessary
        """
