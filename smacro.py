# @version v2.sm.p
# LICENSE: MIT

# keyboard and mouse use references
# https://github.com/moses-palmer/pynput
# https://pythonhosted.org/pynput/
# https://pypi.org/project/pynput/
# https://pynput.readthedocs.io/en/latest/


# you may need to use 'pip install <package>' from some imports:
# pynput, tkinter, serial, threading

import pynput
import time
import sys

import serial
import serial.tools.list_ports

# https://pythonhosted.org/pynput/
from pynput.keyboard import Key, Controller as keyboardController
from pynput.mouse import Button as mouseBtn, Controller as mouseController
from win32gui import GetWindowText, GetForegroundWindow

# message box
import tkinter as tk
from tkinter import messagebox, ttk, Label, Button

import _thread as thread
import threading


# Serial COM
baudrate = 115200
port = ""

# flags, you can also modify with CLI arguments or add in windows shortcut path
defaultActions = False  #* enable default actions, 'global' macros, if dosn't match any open window
showRawRead = False     #? show raw data from Serial interface
showActions = False     #* print action in terminal when a button is presses
debug = False           #? extra debug prints

# listener loop
stop = False


# just to not have a ton of IF's on each handler
def printer(d):
    if debug:
        print(d)

def printAction(action):
    global showActions
    if(showActions == True):
        print(action)



# CL arguments; i know, its messy
printer('Argument List:' + str(sys.argv))
printer(sys.argv)

try:
    i = 1 # the fisrt(0) is the file
    while i < len(sys.argv):
        # -rr - print raw data from serial
        if(sys.argv[i] == '-rr'):
            showRawRead = True
            print("print raw entries enable")
        
        # -sa - enable action printing
        if(sys.argv[i] == '-sa'):
            showActions = True
            print("print actions flag enable")
        
        # -da - enable default actions
        if(sys.argv[i] == '-da'):
            defaultActions = True
            print("default actions enable")

        # -ct - enable print temp in console
        if(sys.argv[i] == '-ct'):
            consoleTemp = True
            print("console temp enabled")
        
        # --debug
        if(sys.argv[i] == '--debug'):
            debug = True
            print("debug prints enable")

        # --port <port>
        if(sys.argv[i] == "--port"):
            # print("not available yet")
            print("port: " + sys.argv[i+1])
            port = sys.argv[i+1]
        
        # --baud <baudrate>
        if(sys.argv[i] == "--baud"):
            # print("not available yet")
            print("baud: " + sys.argv[i+1])
            baudrate = sys.argv[i+1]
        
        # --help / -h
        if(sys.argv[i] == '--help' or sys.argv[i] == '-h'):
            print("-rr | print raw entries [flag]")
            print("-sa | print executed actions [flag]")
            print("-da | enable default actions [flag]")
            print("--debug | enable some prints to help debugging [flag]")
            print("--port <port> | set port where arduino is located (not available)")
            print("\r ex: --port COM9")
            print("--baud <baudrate> | set communication speed")
            print("\r ex: --baud 115200")
            print("--help or -h | print this set of commands help")

        i+=1
    pass
except IndexError:
    printer('no arguments')
    pass


# ? Action handlers
# ? Add profiles as functions and call in listener giving the key code from arduino

# GOOGLE CHROME ACTIONS
def ACTIONS_CHROME (button):
    keyboard = keyboardController()
    
    if button == 'A7':
        keyboard.press(Key.alt)
        keyboard.press(Key.tab)
        keyboard.release(Key.alt)
        keyboard.release(Key.tab)
        printAction(button + "/CHROME: alt tab")

    elif button == 'B0':
        keyboard.press(Key.ctrl)
        keyboard.press('w')
        keyboard.release(Key.ctrl)
        keyboard.release('w')
        printAction(button + "/CHROME: Closing tab")

# DEFAULT ACTIONS IF ANY THE CURRENT WINDOW NOT MATCH ANY PROFILE
def ACTIONS_DEFAULT (button):
    keyboard = keyboardController()
    mouse = mouseController()

    if button == 'A7':
        # keyboard.type('hoi')
        keyboard.press(Key.alt)
        keyboard.press(Key.tab)
        keyboard.release(Key.alt)
        keyboard.release(Key.tab)
        printAction(button + "/default: alt tab")

    elif button == 'B0':
        keyboard.press(Key.ctrl)
        keyboard.press('w')
        keyboard.release(Key.ctrl)
        keyboard.release('w')
        printAction(button + "/default: Closing tab")
        

# ? Serial comm
def startListen(port):
    global stop
    global defaultActions
    global showRawRead
    global baudrate


    # hide window
    root.withdraw()

    ser = serial.Serial(port, baudrate)

    # listener
    while stop == False:

        # current open and active in foreground window 
        currWindow = GetWindowText(GetForegroundWindow())

        try:
            read = ser.readline().strip().decode('ascii')
        except serial.SerialException:
            read = "null"
            stop = ExitApplication(2)
            pass

        if(showRawRead):
            print(currWindow)
            print("raw read: " + read)


        # kill/stop app button, not needed at all
        elif read == 'kil':
            print("stop")
            root.deiconify()
            stop = ExitApplication(1)
            if stop == False:
                root.withdraw()


        #? 'profiles'
        # Add and/or change the name of the program
        # must contain a exactly word of the window title
        if(currWindow.find("Chrome") > -1):
            ACTIONS_CHROME(read)
        # elif(currWindow.find("<My_Program_name_here>")):
            # ACTIOSN_MY_PROGRAM_ACTIONS_HANDLER(read)

        # default actions
        else:
            if(defaultActions): 
                ACTIONS_DEFAULT(read)


# close application
def ExitApplication(reason):
    if reason == 1:
        MsgBox = tk.messagebox.askquestion ('Exit macro','Are you sure you want to exit the app?',icon='warning')
        if MsgBox == 'yes':
            print("exit")
            root.destroy()
            return True
        else:
            return False

    elif reason == 2:
        printer("Serial port disconnected or some error occured. Listener stopped")
        tk.messagebox.showinfo(
            'Error',
            'Serial port device was disconnected or some error occured. Listerner stopped'
        )
        root.destroy()
        return True



# get available ports
avports = []
for por, desc, hwid in sorted(serial.tools.list_ports.comports()):
    avports.append(por)
printer(avports)


class macroThread (threading.Thread):
    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port
    def setPort(self, port):
        self.port = port
    def run(self):
        print("Startig listening for macro entries at port: " + port + ", keep this window open!")
        startListen(port)

listenerThread = macroThread(1, "serial macro listener", "COM1")

#set port and start thread
availableOnce = 0
def setPort():
    global availableOnce
    global port

    if(port == ""):
        printer("port setted by UI")
        port = portsBox.get()

    try:
        ser = serial.Serial(port, baudrate)
        ser.close()

        #init thread
        listenerThread.port = port
        listenerThread.run()
     
        availableOnce+=1
    except serial.SerialException:
        print("port unavailable/busy")
        if(availableOnce > 0):
            printer("stopped")
            stop = True
        pass


# UI
root = tk.Tk()
root.geometry("120x150")
root.title("macro - Select port")

canvas = tk.Canvas(root, width = 200, height = 100)
canvas.pack()

portsBox=ttk.Combobox(root,values=avports,width=10)
portsBox.current(0)

canvas.create_window(55, 20,  window=Label(text="Select Port"))
canvas.create_window(60, 40,  window=portsBox)
canvas.create_window(60, 70,  window=Button(text="Macro",command=setPort))


if port == "":
    root.mainloop()
else:
    printer("port set by CLI")
    setPort()

