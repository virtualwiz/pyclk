# Copyright (C) 2018 Shangming Du, University of Birmingham. All Rights Reserved.
#  ____         ____ _     _  __
# |  _ \ _   _ / ___| |   | |/ /
# | |_) | | | | |   | |   | ' /
# |  __/| |_| | |___| |___| . \
# |_|    \__, |\____|_____|_|\_\
#        |___/
#
# PYCLK, SpecialClock with GUI.
# https://github.com/virtualwiz/pyclk Kept PRIVATE before submission
# ================================================================================

# Import dependencies. Prompt user if Python version isn't correct
try:
    import sys
    import tkinter as tk # Main GUI library
    from tkinter import ttk # Submodule of tkinter
    from tkinter import messagebox # Reminder messagebox for Countdown
    import time
    import datetime as rtc # Date and time library
    import threading
    import webbrowser
except:
    print("Sorry, some dependencies are not met.")
    print("Can you call this application with Python>=3.1?")
    sys.exit()

Application_Window_Width = 400
Application_Window_Height = 220

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

class Timer_Common():
    Reading = ""
    Is_Running = False

    def Get_Time(self):
        # Get Unix Since Epoch Time (.1s)
        return int(time.time() * 10)

    def Convert_Time(self, One_Tenth_Seconds):
        # Convert to time format from an integer (seconds/10)
        intervals = [26000, 600, 10, 1]
        result=[]
        for unit in intervals:
            val = One_Tenth_Seconds // unit
            One_Tenth_Seconds -= val * unit
            result.append("{}".format(val))
        return result[0] + ":" + result[1] + ":" + result[2] + "." + result[3]

class STPW(Timer_Common):
    def __init__(self):
        # Start countdown thread on CTDN instance creation
        self.Mark_BeginOfPeriod = self.Get_Time()
        self.Mark_EndOfPeriod = self.Get_Time()
        self.Pause_Buffer = 0
        self.Stopwatch_Thread_Start()

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

    def Stopwatch_Loop(self):
        while True:
            if self.Is_Running:
                self.Reading = self.Convert_Time(self.Get_Time() - self.Mark_BeginOfPeriod)
            else:
                self.Reading = self.Convert_Time(self.Mark_EndOfPeriod - self.Mark_BeginOfPeriod)
            time.sleep(0.1)

    def Stopwatch_Thread_Start(self):
        self.Stopwatch_Thread = threading.Thread(target=self.Stopwatch_Loop)
        self.Stopwatch_Thread.start()

STPW_Instance = STPW()

class CTDN(Timer_Common):
    def __init__(self):
        # Start countdown thread on CTDN instance creation
        self.Count_Thread_Start()
        self.Mark_CountSet = self.Get_Time()
        self.Mark_CountTerminating = self.Get_Time()
        self.Delta = 0

    def Mark(self, Var, TimeDelta=0):
        # Write time reading into a variable
        if Var == "set":
            self.Mark_CountSet = self.Get_Time() + TimeDelta
        elif Var == "term":
            self.Mark_CountTerminating = self.Get_Time() + TimeDelta

    def Command(self, Cmd):
        # Countdown commands
        try:
            Entry_NaN = False
            self.Delta = int(PYCLK_Window.StringVar_CTDN_Hset.get())*36000+int(PYCLK_Window.StringVar_CTDN_Mset.get())*600+int(PYCLK_Window.StringVar_CTDN_Sset.get())*10
        except:
            Entry_NaN = True

        if Cmd == "set" and self.Delta !=0 and Entry_NaN == False:
            self.Mark("set")
            self.Mark("term", TimeDelta = self.Delta)
            self.Is_Running = True
        elif Cmd == "reset":
            self.Mark("set")
            self.Mark("term")
            self.Is_Running = False

    def Count_Loop(self):
        while True:
            # self.Update_Buttons_State()
            if self.Is_Running:
                if(self.Get_Time() != self.Mark_CountTerminating):
                    self.Reading = self.Convert_Time(self.Mark_CountTerminating - self.Get_Time())
                else:
                    messagebox.showinfo("Message from PyCLK", "Time is up in your Countdown Timer session.")
                    self.Is_Running = False
            else:
                self.Reading = "READY"
            time.sleep(0.1)

    def Count_Thread_Start(self):
        self.Count_Thread = threading.Thread(target=self.Count_Loop)
        self.Count_Thread.start()

CTDN_Instance = CTDN()

class PYCLK(tk.Tk):
    def __init__(self):
        super().__init__()
        # Interact with System Window Manager to set window size and title
        # Disable main window resizing
        self.title("PyCLK")
        self.geometry(str(Application_Window_Width)+"x"+str(Application_Window_Height))
        self.resizable(True, True)

        # Create tabbed Notebook widget and add Frames as Notebook pages
        self.Main_Notebook = ttk.Notebook(self)
        self.Page_TIME = ttk.Frame(self.Main_Notebook)
        self.Page_STPW = ttk.Frame(self.Main_Notebook)
        self.Page_CTDN = ttk.Frame(self.Main_Notebook)
        self.Page_ABRT = ttk.Frame(self.Main_Notebook)
        self.Main_Notebook.add(self.Page_TIME, text="Time")
        self.Main_Notebook.add(self.Page_STPW, text="Stopwatch")
        self.Main_Notebook.add(self.Page_CTDN, text="Countdown")
        self.Main_Notebook.add(self.Page_ABRT, text="Abort")
        self.Main_Notebook.pack(expand=1, fill="both")

        # Widgets on page Time
        self.StringVar_TIME_Clock = tk.StringVar()
        self.StringVar_TIME_Date = tk.StringVar()
        self.StringVar_TIME_AmPm = tk.StringVar()
        self.Widget_TIME_Clock = tk.Label(self.Page_TIME, textvariable=self.StringVar_TIME_Clock, font=("", 70))
        self.Widget_TIME_Date = tk.Label(self.Page_TIME, textvariable=self.StringVar_TIME_Date, font=("", 30))
        self.Widget_TIME_TimeFormat = tk.Checkbutton(self.Page_TIME, text="24h Format")
        self.Widget_TIME_AmPm = tk.Label(self.Page_TIME, textvariable=self.StringVar_TIME_AmPm, font=("", 30))
        self.Widget_TIME_Clock.place(relx=0, rely=0, relheight=0.5, relwidth=1)
        self.Widget_TIME_Date.place(relx=0, rely=0.5, relheight=0.25, relwidth=1)
        self.Widget_TIME_TimeFormat.place(relx=0, rely=0.75, relheight=0.25, relwidth=0.2)
        self.Widget_TIME_AmPm.place(relx=0.8, rely=0.75, relheight=0.25, relwidth=0.2)

        # Widgets on page Stopwatch
        self.StringVar_STPW_CurrentReading = tk.StringVar()
        self.StringVar_STPW_CurrentReading.set("N/A")
        self.Widget_STPW_Display = tk.Label(self.Page_STPW, textvariable=self.StringVar_STPW_CurrentReading, font=("", 50))
        self.Widget_STPW_StartButton = tk.Button(self.Page_STPW, text="Start\nResume", activebackground="#8EFF94", command=lambda:STPW_Instance.Command("start"))
        self.Widget_STPW_PauseResetButton = tk.Button(self.Page_STPW, text="Pause\nReset", activebackground="#FFADAD", command=lambda:STPW_Instance.Command("pausereset"))
        self.Widget_STPW_LogButton = tk.Button(self.Page_STPW, text="Log",activebackground="#F9FF8E", command=lambda:STPW_Instance.Command("log"))
        self.Widget_STPW_LogDisplay = tk.Listbox(self.Page_STPW)
        self.Widget_STPW_Display.place(relx=0, rely=0, relheight=0.6, relwidth=0.75)
        self.Widget_STPW_StartButton.place(relx=0, rely=0.6, relheight=0.4, relwidth=0.25)
        self.Widget_STPW_PauseResetButton.place(relx=0.25, rely=0.6, relheight=0.4, relwidth=0.25)
        self.Widget_STPW_LogButton.place(relx=0.5, rely=0.6, relheight=0.4, relwidth=0.25)
        self.Widget_STPW_LogDisplay.place(relx=0.75, rely=0, relheight=1, relwidth=0.25)

        #Widgets on page Countdown
        self.StringVar_CTDN_CurrentReading = tk.StringVar()
        self.StringVar_CTDN_CurrentReading.set("N/A")
        self.StringVar_CTDN_Hset = tk.StringVar()
        self.StringVar_CTDN_Mset = tk.StringVar()
        self.StringVar_CTDN_Sset = tk.StringVar()
        self.StringVar_CTDN_Hset.set("0")
        self.StringVar_CTDN_Mset.set("0")
        self.StringVar_CTDN_Sset.set("0")
        self.Widget_CTDN_Display = tk.Label(self.Page_CTDN, textvariable=self.StringVar_CTDN_CurrentReading, font=("", 70))
        self.Widget_CTDN_HEntry = tk.Entry(self.Page_CTDN, textvariable=self.StringVar_CTDN_Hset)
        self.Widget_CTDN_MEntry = tk.Entry(self.Page_CTDN, textvariable=self.StringVar_CTDN_Mset)
        self.Widget_CTDN_SEntry = tk.Entry(self.Page_CTDN, textvariable=self.StringVar_CTDN_Sset)
        self.Widget_CTDN_HLabel = tk.Label(self.Page_CTDN, text="H")
        self.Widget_CTDN_MLabel = tk.Label(self.Page_CTDN, text="M")
        self.Widget_CTDN_SLabel = tk.Label(self.Page_CTDN, text="S")
        self.Widget_CTDN_StartButton = tk.Button(self.Page_CTDN, text="Set and\nStart", command=lambda:CTDN_Instance.Command("set"))
        self.Widget_CTDN_CancelButton = tk.Button(self.Page_CTDN, text="Cancel", command=lambda:CTDN_Instance.Command("reset"))
        self.Widget_CTDN_Display.place(relx=0, rely=0, relheight=0.75, relwidth=1)
        self.Widget_CTDN_HEntry.place(relx=0, rely=0.75, relheight=0.25, relwidth=0.16)
        self.Widget_CTDN_MEntry.place(relx=0.2, rely=0.75, relheight=0.25, relwidth=0.16)
        self.Widget_CTDN_SEntry.place(relx=0.4, rely=0.75, relheight=0.25, relwidth=0.16)
        self.Widget_CTDN_HLabel.place(relx=0.16, rely=0.75, relheight=0.25, relwidth=0.04)
        self.Widget_CTDN_MLabel.place(relx=0.36, rely=0.75, relheight=0.25, relwidth=0.04)
        self.Widget_CTDN_SLabel.place(relx=0.56, rely=0.75, relheight=0.25, relwidth=0.04)
        self.Widget_CTDN_StartButton.place(relx=0.6, rely=0.75, relheight=0.25, relwidth=0.2)
        self.Widget_CTDN_CancelButton.place(relx=0.8, rely=0.75, relheight=0.25, relwidth=0.2)

        # Widgets on page Abort
        self.Widget_ABRT_Abort = tk.Label(self.Page_ABRT, text="Designed by Shangming Du\nSchool of Engineering\nUniversity of Birmingham\nDec.06 2018\n\nRemote Git Repository:\nhttps://github.com/virtualwiz/pyclk\n")
        self.Widget_ABRT_VisitButton = tk.Button(self.Page_ABRT, text="Visit GitHub Page of PyCLK", command=lambda:webbrowser.open_new("https://github.com/virtualwiz/pyclk"))
        self.Widget_ABRT_Abort.place(relx=0, rely=0, relheight=0.8, relwidth=1)
        self.Widget_ABRT_VisitButton.place(relx=0, rely=0.8, relheight=0.2, relwidth=1)

        # Start Threads
        self.TIME_Refresh_Loop_Start()
        self.STPW_Refresh_Loop_Start()
        self.CTDN_Refresh_Loop_Start()

    def TIME_Refresh_Loop(self):
        while True:
            try:
                self.StringVar_TIME_Clock.set(TIME_Instance.TimeString)
                self.StringVar_TIME_Date.set(TIME_Instance.DateString)
            except RuntimeError:
                sys.exit()
            time.sleep(1)

    def TIME_Refresh_Loop_Start(self):
        self.TIME_Thread = threading.Thread(target=self.TIME_Refresh_Loop)
        self.TIME_Thread.start()

    def STPW_Refresh_Loop(self):
        while True:
            try:
                self.StringVar_STPW_CurrentReading.set(STPW_Instance.Reading)
            except RuntimeError:
                sys.exit()
            time.sleep(0.1)

    def STPW_Refresh_Loop_Start(self):
        self.STPW_Thread = threading.Thread(target=self.STPW_Refresh_Loop)
        self.STPW_Thread.start()

    def CTDN_Refresh_Loop(self):
        while True:
            try:
                if CTDN_Instance.Is_Running:
                    self.Widget_CTDN_StartButton.config(state="disabled")
                    self.Widget_CTDN_CancelButton.config(state="normal")
                else:
                    self.Widget_CTDN_StartButton.config(state="normal")
                    self.Widget_CTDN_CancelButton.config(state="disabled")
                self.StringVar_CTDN_CurrentReading.set(CTDN_Instance.Reading)
            except RuntimeError:
                sys.exit()
            time.sleep(0.1)

    def CTDN_Refresh_Loop_Start(self):
        self.CTDN_Thread = threading.Thread(target=self.CTDN_Refresh_Loop)
        self.CTDN_Thread.start()

PYCLK_Window = PYCLK()

# Main application goes event-driven
PYCLK_Window.mainloop()

