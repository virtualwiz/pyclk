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

# Import dependencies. Prompt user if Python version isn't correct
try:
    import tkinter as tk # Main GUI library
    from tkinter import ttk # Submodule of tkinter
    import time
    import datetime as rtc # Date and time library
    import threading
    import sys
except:
    print("Sorry, some dependencies are not met.")
    print("Can you call this application with Python>=3.1?")
    exit()
    
# Flags(Signals) to operate all threads
Application_Terminate_Signal = False
Application_Window_Width = 400
Application_Window_Height = 220
Application_Debug = True

class TIME():
    def __init__(self):
        # Start ticking thread on TIME instance creation
        self.Tick_Thread_Start()

    def Tick_Loop(self):
        while True:
            self.DateTime_Now = rtc.datetime.now()
            self.TimeString = self.DateTime_Now.strftime("%H:%M:%S")
            self.DateString = self.DateTime_Now.strftime("%a,%d %B %Y")
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
        self.title("PYCLK")
        self.geometry(str(Application_Window_Width)+"x"+str(Application_Window_Height))
        self.resizable(True, True)

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

        # Widgets on page Time
        self.StringVar_TIME_Clock = tk.StringVar()
        self.StringVar_TIME_Date = tk.StringVar()
        Widget_TIME_Clock = tk.Label(Page_TIME, textvariable=self.StringVar_TIME_Clock, font=("", 70))
        Widget_TIME_Date = tk.Label(Page_TIME, textvariable=self.StringVar_TIME_Date, font=("", 30))
        Widget_TIME_TimezoneLabel = tk.Label(Page_TIME, text="Timezone")
        Widget_TIME_Timezone = tk.Label(Page_TIME, text="Placeholder")
        Widget_TIME_TimeFormat = tk.Checkbutton(Page_TIME, text="24h Format")
        Widget_TIME_QuitButton = tk.Button(Page_TIME, text="Quit")
        Widget_TIME_Clock.place(relx=0, rely=0, relheight=0.5, relwidth=1)
        Widget_TIME_Date.place(relx=0, rely=0.5, relheight=0.25, relwidth=1)
        Widget_TIME_TimezoneLabel.place(relx=0, rely=0.75, relheight=0.25, relwidth=0.2)
        Widget_TIME_Timezone.place(relx=0.2, rely=0.75, relheight=0.25, relwidth=0.4)
        Widget_TIME_TimeFormat.place(relx=0.6, rely=0.75, relheight=0.25, relwidth=0.2)
        Widget_TIME_QuitButton.place(relx=0.8, rely=0.75, relheight=0.25, relwidth=0.2)

        # Widgets on page Stopwatch
        self.StringVar_STPW_CurrentReading = tk.StringVar()
        self.StringVar_STPW_CurrentReading.set("00:00.0")
        Widget_STPW_Display = tk.Label(Page_STPW, textvariable=self.StringVar_STPW_CurrentReading, font=("", 50))
        Widget_STPW_StartButton = tk.Button(Page_STPW, text="Start", activebackground="#8EFF94")
        Widget_STPW_StopResetButton = tk.Button(Page_STPW, text="Stop\nReset", activebackground="#FFADAD")
        Widget_STPW_LogButton = tk.Button(Page_STPW, text="Log",activebackground="#F9FF8E")
        Widget_STPW_LogDisplay = tk.Listbox(Page_STPW)
        Widget_STPW_Display.place(relx=0, rely=0, relheight=0.6, relwidth=0.6)
        Widget_STPW_StartButton.place(relx=0, rely=0.6, relheight=0.4, relwidth=0.2)
        Widget_STPW_StopResetButton.place(relx=0.2, rely=0.6, relheight=0.4, relwidth=0.2)
        Widget_STPW_LogButton.place(relx=0.4, rely=0.6, relheight=0.4, relwidth=0.2)
        Widget_STPW_LogDisplay.place(relx=0.6, rely=0, relheight=1, relwidth=0.4)

        #Widgets on page Countdown
        self.StringVar_CTDN_CurrentReading = tk.StringVar()
        self.StringVar_CTDN_CurrentReading.set("HH:MM:SS")
        Widget_CTDN_Display = tk.Label(Page_CTDN, textvariable=self.StringVar_CTDN_CurrentReading, font=("", 70))
        Widget_CTDN_HEntry = tk.Entry(Page_CTDN)
        Widget_CTDN_MEntry = tk.Entry(Page_CTDN)
        Widget_CTDN_SEntry = tk.Entry(Page_CTDN)
        Widget_CTDN_HLabel = tk.Label(Page_CTDN, text="H")
        Widget_CTDN_MLabel = tk.Label(Page_CTDN, text="M")
        Widget_CTDN_SLabel = tk.Label(Page_CTDN, text="S")
        Widget_CTDN_StartButton = tk.Button(Page_CTDN, text="Set and\nStart", activebackground="#8EFF94")
        Widget_CTDN_CancelButton = tk.Button(Page_CTDN, text="Cancel", activebackground="#FFADAD")
        Widget_CTDN_Display.place(relx=0, rely=0, relheight=0.75, relwidth=1)
        Widget_CTDN_HEntry.place(relx=0, rely=0.75, relheight=0.25, relwidth=0.16)
        Widget_CTDN_MEntry.place(relx=0.2, rely=0.75, relheight=0.25, relwidth=0.16)
        Widget_CTDN_SEntry.place(relx=0.4, rely=0.75, relheight=0.25, relwidth=0.16)
        Widget_CTDN_HLabel.place(relx=0.16, rely=0.75, relheight=0.25, relwidth=0.04)
        Widget_CTDN_MLabel.place(relx=0.36, rely=0.75, relheight=0.25, relwidth=0.04)
        Widget_CTDN_SLabel.place(relx=0.56, rely=0.75, relheight=0.25, relwidth=0.04)
        Widget_CTDN_StartButton.place(relx=0.6, rely=0.75, relheight=0.25, relwidth=0.2)
        Widget_CTDN_CancelButton.place(relx=0.8, rely=0.75, relheight=0.25, relwidth=0.2)
        

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

