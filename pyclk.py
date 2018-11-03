# Copyright (C) 2018 Shangming Du, University of Birmingham. All Rights Reserved.
#
# PYCLK, SpecialClock with GUI.
# https://github.com/virtualwiz/pyclk
# ================================================================================

import tkinter as tk # Main GUI library
from tkinter import ttk # Submodule of tkinter

import time
import datetime as rtc # Date and time library
import threading

class PYCLK(tk.Tk):
    def __init__(self):
        super().__init__()
        # Interact with System Window Manager to set window size and title
        # Disable main window resizing
        self.geometry("480x320")
        self.title("PYCLK")
        self.resizable(False, False)

        # Create tabbed Notebook widget and add Frames as Notebook pages
        Main_Notebook = ttk.Notebook(self)
        Page_TIME = ttk.Frame(Main_Notebook)
        Page_STPW = ttk.Frame(Main_Notebook)
        Page_CTDN = ttk.Frame(Main_Notebook)
        Page_ALRM = ttk.Frame(Main_Notebook)
        Main_Notebook.add(Page_TIME, text="Time")
        Main_Notebook.add(Page_STPW, text="Stopwatch")
        Main_Notebook.add(Page_CTDN, text="Countdown")
        Main_Notebook.add(Page_ALRM, text="Alarm")
        Main_Notebook.pack(expand=1, fill="both")

        # TestLabel = tk.Label(Page_TIME, text=TIME.HH)
        # TestLabel.pack()

        # TestThing = tk.Button(Page_STPW, text=TIME.YYYY)
        # TestThing.pack()
        

class TIME():
    # Initialise Time Attributes
    DateTime_Now = None
    TimeString = ''
    DateString = ''

    def Refetch_From_RTC(self):
        DateTime_Now = rtc.datetime.now()

    def Refresh_Strings(self):
        pass

class CTDN():
    pass
    


if __name__ == "__main__":
    Main_Window = PYCLK()
    Main_Window.mainloop()