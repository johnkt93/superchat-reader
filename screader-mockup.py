import tkinter
import tkinter.ttk as ttk
import logging

__version__ = (0,1,0)

running = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d [%(levelname)8s] %(message)s",
    datefmt="%m/%d %H:%M:%S")
)
logger.addHandler(consoleHandler)

configWindow = tkinter.Tk()
chatWindow = tkinter.Tk()
configWindow.focus_force()

chatWindowShown = True
def toggleChatWindow ():
    global chatWindowShown
    if chatWindow.state() == 'normal':
        chatWindow.withdraw()
        chatWindowShown = False
    elif chatWindow.state() == 'withdrawn':
        chatWindow.deiconify()
        configWindow.focus_force()
        chatWindowShown = True
    logger.debug(chatWindow.state())

def showGeometries():
    logger.info("config Window " + configWindow.geometry())
    logger.info("chat Window   " + chatWindow.geometry())

def stopMainLoop():
    global logger
    global running
    logger.info("Shutdown")
    running = False

configWindow.title(f"Superchat Reader v{__version__[0]}.{__version__[1]}")
configWindow.wm_grid(widthInc=400,heightInc=40)

##################
## Menu Bar Setup
menuMain = tkinter.Menu(master=configWindow)
configWindow.config(menu=menuMain)

menuFile = tkinter.Menu(master=menuMain, tearoff=0)
menuMain.add_cascade(label="File", menu=menuFile)
menuFile.add_command(label="Open...")
menuFile.add_command(label="Save...")
menuFile.add_command(label="Save with images...")
menuFile.add_separator()
menuFile.add_command(label="Print Geometries", command=showGeometries)
menuFile.add_command(label="Quit", command=stopMainLoop)


menuView = tkinter.Menu(master=menuMain, tearoff=0)
# This doesn't work correctly, it doesn't check/uncheck based on the variable OR the window state
menuView.add_checkbutton(label="Show Chat Messages", command=toggleChatWindow, variable=chatWindowShown)
menuMain.add_cascade(label="View", menu=menuView)

menuConnect = tkinter.Menu(master=menuMain, tearoff=0)
menuConnect.add_command(label="Add new account")
menuConnect.add_command(label="Import messages from video")
menuMain.add_cascade(label="Connect", menu=menuConnect)


##################
## Config Window Setup
frameAccounts = ttk.Frame(master=configWindow)
frameAccounts.grid(column=0,row=0,rowspan=40)

ttk.Label(master=frameAccounts, text="YT Account 1").pack()
ttk.Label(master=frameAccounts, text="YT Account 2").pack()
ttk.Label(master=frameAccounts, text="Stream Elements Account 1").pack()
ttk.Label(master=frameAccounts, text="Stream Labs Account 1").pack()
ttk.Button(master=frameAccounts, text="+ Add Account").pack()

frameStreams = ttk.Frame(configWindow)
frameStreams.grid(column=1,row=0)

ttk.Label(master=frameStreams, text="Video 1").pack()
ttk.Label(master=frameStreams, text="Video 2").pack()
ttk.Label(master=frameStreams, text="Video 3 mbik1dnv5T8").pack()
ttk.Button(master=frameStreams, text="Refresh Videos").pack()


##################
## Chat Window Setup
chatWindow.title("Messages")
ttk.Label(master=chatWindow,text="Message 1").pack()
ttk.Label(master=chatWindow,text="Message 2").pack()
ttk.Label(master=chatWindow,text="Message 3").pack()
ttk.Label(master=chatWindow,text="Message 4").pack()

def updateWindows():
    try:
        configWindow.update_idletasks()
        configWindow.update()
        chatWindow.update_idletasks()
        chatWindow.update()
    except:
        logger.warning("Failed to update windows (this is normal while quitting the program)")

configWindow.protocol("WM_DELETE_WINDOW", stopMainLoop)
chatWindow.protocol("WM_DELETE_WINDOW", toggleChatWindow)

updateWindows()
chatWindow.geometry(f"600x400+{configWindow.winfo_x() + configWindow.winfo_width() + 20}+{configWindow.winfo_y()}")
showGeometries()

logger.info("Starting main loop")

while running:
    updateWindows()

configWindow.quit()
