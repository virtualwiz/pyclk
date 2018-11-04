# Copyright (C) 2018 Shangming Du, University of Birmingham. All Rights Reserved.
#  ____         ____ _     _  __
# |  _ \ _   _ / ___| |   | |/ /
# | |_) | | | | |   | |   | ' / 
# |  __/| |_| | |___| |___| . \ 
# |_|    \__, |\____|_____|_|\_\
#        |___/
# 
# PYCLK, SpecialClock with GUI.
# https://github.com/virtualwiz/pyclk
# ================================================================================

import tkinter as tk # Main GUI library
from tkinter import ttk # Submodule of tkinter
import time
import datetime as rtc # Date and time library
import threading
import sys

# Flags(Signals) to operate all threads
Application_Terminate_Signal = False

class TIME():
    def __init__(self):
        # Initialise Time Variables
        # DateTime_Now = None
        # self.TimeString = 'initTime'
        # self.DateString = 'initDate'
        self.Tick_Thread_Start()

    def Tick_Loop(self):
        while True:
            self.DateTime_Now = rtc.datetime.now()
            self.TimeString = self.DateTime_Now.strftime("%H:%M:%S")
            self.DateString = self.DateTime_Now.strftime("%a, %m %B %Y")
            time.sleep(1)

    def Tick_Thread_Start(self):
        self.Tick_Thread = threading.Thread(target=self.Tick_Loop)
        self.Tick_Thread.start()


TIME_Instance = TIME()


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

        # Widgets on TIME page
        self.StringVar_TIME_Clock = tk.StringVar()
        self.StringVar_TIME_Date = tk.StringVar()
        Widget_TIME_Clock = tk.Label(Page_TIME, textvariable=self.StringVar_TIME_Clock, font=("Courier", 80))
        Widget_TIME_Date = tk.Label(Page_TIME, textvariable=self.StringVar_TIME_Date, font=("Courier", 30))
        Widget_TIME_TimezoneLabel = tk.Label(Page_TIME, text="Timezone")
        Widget_TIME_Timezone = tk.Label(Page_TIME, text="Placeholder")
        Widget_TIME_TimeFormat = tk.Checkbutton(Page_TIME, text="24h Format")
        Widget_TIME_QuitButton = tk.Button(Page_TIME, text="Quit", command=sys.exit)
        Widget_TIME_Clock.grid(row=1, column=1, columnspan=4, sticky="nsew", padx=10, pady=3)
        Widget_TIME_Date.grid(row=2, column=1, columnspan=4,sticky="nsew", padx=10, pady=3)
        Widget_TIME_TimezoneLabel.grid(row=3, column=1, sticky="W")
        Widget_TIME_Timezone.grid(row=3, column=2, sticky="W")
        Widget_TIME_TimeFormat.grid(row=3, column=3, sticky="W")
        Widget_TIME_QuitButton.grid(row=3, column=4, sticky="E")

        # Widgets on STPW page
        # Widget_STPW_Display = tk.Label(Page_STPW, text="alskjdfkljashfdkjhaskldfhlaskjdfhlkajshfdkjaslkdjfhlaskdhflksjahfdkjlashdfkjhaslkdfhlaskjdhflkasjhfkjashfdkjhalsdjfh")
        # Widget_STPW_Display.pack()
        

        # Start Threads
        self.TIME_Thread_Start()

    def TIME_Loop(self):
        while True:
            self.StringVar_TIME_Clock.set(TIME_Instance.TimeString)
            self.StringVar_TIME_Date.set(TIME_Instance.DateString)
            time.sleep(1)

    def TIME_Thread_Start(self):
        self.TIME_Thread = threading.Thread(target=self.TIME_Loop)
        self.TIME_Thread.start()

PYCLK_Window = PYCLK()

# Main application goes event-driven
PYCLK_Window.mainloop()

