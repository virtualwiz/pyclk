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
    import sys
    import tkinter as tk # Main GUI library
    from tkinter import ttk # Submodule of tkinter
    import time
    import datetime as rtc # Date and time library
    import threading
except:
    print("Sorry, some dependencies are not met.")
    print("Can you call this application with Python>=3.1?")
    sys.exit()

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

class STPW():
    def __init__(self):
        # Start countdown thread on CTDN instance creation
        self.Reading = "READY"
        self.Mark_BeginOfPeriod = self.Get_Time()
        self.Mark_EndOfPeriod = self.Get_Time()
        self.Pause_Buffer = 0
        self.Is_Running = False
        self.Stopwatch_Thread_Start()

    def Get_Time(self):
        # Get Unix Since Epoch Time(.1s)
        return int(time.time() * 10)

    def Mark(self, Var):
        # Write time reading into a variable
        if Var == "begin":
            self.Mark_BeginOfPeriod = self.Get_Time()
        elif Var == "end":
            self.Mark_EndOfPeriod = self.Get_Time()

    def Command(self, Cmd):
        # Stopwatch commands
        if Cmd == "start":
            if self.Is_Running == False: # Stopwatch is not running (pause or idle)
                self.Is_Running = True
                if self.Mark_BeginOfPeriod != self.Mark_EndOfPeriod: # Paused state
                    self.Pause_Buffer = self.Mark_EndOfPeriod - self.Mark_BeginOfPeriod
                    self.Mark("begin")
                    self.Mark_BeginOfPeriod -= self.Pause_Buffer;
                else: # Idle state
                    self.Mark("begin")
        elif Cmd == "pausereset":
            if self.Is_Running == False:
                # Reset the stopwatch
                PYCLK_Window.Widget_STPW_LogDisplay.delete(0, tk.END)
                self.Mark("begin")
                self.Mark("end")
            else:
                # Stop the stopwatch
                self.Mark("end")
                self.Is_Running = False
        elif Cmd == "log":
            PYCLK_Window.Widget_STPW_LogDisplay.insert(tk.END, self.Reading)

    def Convert_Time(self, One_Tenth_Seconds):
        # Convert to time format from an integer (seconds/10)
        intervals = [26000, 600, 10, 1]
        result=[]
        for unit in intervals:
            val = One_Tenth_Seconds // unit
            One_Tenth_Seconds -= val * unit
            result.append("{}".format(val))
        return result[0] + ":" + result[1] + ":" + result[2] + ":" + result[3]

    def Stopwatch_Loop(self):
        while True:
            if self.Is_Running:
                self.Reading = self.Convert_Time(self.Get_Time() - self.Mark_BeginOfPeriod)
            else:
                self.Reading = self.Convert_Time(self.Mark_EndOfPeriod - self.Mark_BeginOfPeriod)
            time.sleep(0.1)
        pass

    def Stopwatch_Thread_Start(self):
        self.Stopwatch_Thread = threading.Thread(target=self.Stopwatch_Loop)
        self.Stopwatch_Thread.start()

STPW_Instance = STPW()

class CTDN():
    def __init__(self):
        # Start countdown thread on CTDN instance creation
        self.Count_Thread_Start()

    def Count_Loop(self):
        pass

    def Count_Thread_Start(self):
        pass

CTDN_Instance = CTDN()

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
        Widget_STPW_StartButton = tk.Button(Page_STPW, text="Start\nResume", activebackground="#8EFF94", command=lambda:STPW_Instance.Command("start"))
        Widget_STPW_PauseResetButton = tk.Button(Page_STPW, text="Pause\nReset", activebackground="#FFADAD", command=lambda:STPW_Instance.Command("pausereset"))
        Widget_STPW_LogButton = tk.Button(Page_STPW, text="Log",activebackground="#F9FF8E", command=lambda:STPW_Instance.Command("log"))
        self.Widget_STPW_LogDisplay = tk.Listbox(Page_STPW)
        Widget_STPW_Display.place(relx=0, rely=0, relheight=0.6, relwidth=0.75)
        Widget_STPW_StartButton.place(relx=0, rely=0.6, relheight=0.4, relwidth=0.25)
        Widget_STPW_PauseResetButton.place(relx=0.25, rely=0.6, relheight=0.4, relwidth=0.25)
        Widget_STPW_LogButton.place(relx=0.5, rely=0.6, relheight=0.4, relwidth=0.25)
        self.Widget_STPW_LogDisplay.place(relx=0.75, rely=0, relheight=1, relwidth=0.25)

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
        self.TIME_Refresh_Loop_Start()
        self.STPW_Refresh_Loop_Start()

    def TIME_Refresh_Loop(self):
        while True:
            self.StringVar_TIME_Clock.set(TIME_Instance.TimeString)
            self.StringVar_TIME_Date.set(TIME_Instance.DateString)
            time.sleep(1)

    def TIME_Refresh_Loop_Start(self):
        self.TIME_Thread = threading.Thread(target=self.TIME_Refresh_Loop)
        self.TIME_Thread.start()

    def STPW_Refresh_Loop(self):
        while True:
            self.StringVar_STPW_CurrentReading.set(STPW_Instance.Reading)
            time.sleep(0.1)

    def STPW_Refresh_Loop_Start(self):
        self.STPW_Thread = threading.Thread(target=self.STPW_Refresh_Loop)
        self.STPW_Thread.start()

    # def STPW_Refresh_LogDisplay(self):
    #     self.Widget_STPW_LogDisplay.insert(tk.END, "something") 

PYCLK_Window = PYCLK()

# Main application goes event-driven
PYCLK_Window.mainloop()

