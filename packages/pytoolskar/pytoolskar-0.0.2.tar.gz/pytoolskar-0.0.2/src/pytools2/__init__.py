__version__ = 1.02
try:
    import tkinter as tk
    BOTTOM_TK = tk.BOTTOM
    TOP_TK = tk.TOP
    LEFT_TK = tk.LEFT
    RIGHT_TK = tk.RIGHT
except ImportError:
    pass
class PyToolsError(Exception): pass

"""

#############################################################
                         PyTools
                     Copyright (Date)
                 Created by KareemTheBest
#############################################################

"""

# PyTools is an tool for Python. It runs advanced and
# regular commands. It was made for people to slowly but
# surely get better at Python. PyTools is simple to learn
# and is recommended for people. Goodbye (and adios!)
def moduleset(module='py'): 'Module set.'; return __import__(module)
def rsttomovobj(x=0,y=0,object=None):
	'Call a rtmo (rest to move object) event. Works only with Tk objects'
	try:
		if type(object) is tk.Tk:
			import warnings as warn
			warn.warn("Because object's type is tk.Tk, this warning is called.", Warning, 2)
		else:
			object.place(x=x,y=y)
	except NameError:
		import warnings as warn
		warn.warn("Because you do not have tkinter installed, this warning is called.", Warning, 2)
def convert(file):
    """Converts a Python file to an executable. Make sure to add the directory."""
    import os
    download = input("This command requires PyInstaller to work. Install PyInstaller?: ")
    if download == 'Yes' or download == 'yes':
        downloadcmd = "%USERPROFILE%/AppData/Local/Programs/Python/Python39/Scripts/pip install pyinstaller"
        os.system(downloadcmd)
    elif download == 'No' or download == 'no':
        pass
    try:
        cmd = "%USERPROFILE%/AppData/Local/Programs/Python/Python39/Scripts/pyinstaller.exe -F "+file+".py"
        os.system(cmd)
    except SyntaxError:
        raise PyToolsError('PyInstaller does not exist')

def install(module):
    """Installs a module to Python."""
    cmd = "%USERPROFILE%/AppData/Local/Programs/Python/Python39/Scripts/pip install " + module
    import os
    os.system(cmd)

def uninstall(module):
    """Uninstalls a module from Python."""
    cmd = "%USERPROFILE%/AppData/Local/Programs/Python/Python39/Scripts/pip uninstall " + module
    import os
    os.system(cmd)

def write(file, contents='', filetype=''):
    """Writes contents to a file."""
    with open(file + '.' + filetype, 'a') as f:
        f.write(contents)
        f.close()

def read(file, filetype):
    """Reads contents of a file."""
    length = 999999999
    with open(file + '.' + filetype, 'r') as f:
        read = f.read(int(length))
        f.seek(0)
        print(read)
        f.close()
        
def create(file, contents='', filetype=''):
    """Creates a file. Contents will be added to a file if it already exists."""
    with open(file + '.' + filetype, 'a') as f:
        f.write(contents)
        f.close()
        
def overwrite(file, contents='', filetype=''):
    """Overwrites a file. Replaces the old contents with the new ones."""
    with open(file + '.' + filetype, 'w') as f:
        f.write(contents)
        f.close()

def reverse(text=''):
    """Reverses text."""
    global REVERSED
    textlist = list(text)
    textlist.reverse()
    reversedtext = ""
    for i in range(0, len(text)):
        reversedtext = reversedtext + textlist[i]
    REVERSED = reversedtext
    print(REVERSED)
    
"""
#############################################################
                      Advanced Commands
#############################################################
"""
def prompt():
    """Runs a window of command prompt."""
    import os
    os.system('cmd.exe')

def error(ExceptionError):
    """Runs an exception error."""
    raise ExceptionError

def powershell():
    """Runs a window of PowerShell."""
    import os
    os.system('powershell.exe')

def pytoolsprompt():
    """Runs a window of PyTools Prompt."""
    import os
    os.system('cmd.exe /f %USERPROFILE%/AppData/Local/Programs/Python/Python39/Lib/site-packages/pytools2/pytprompt.py')

def pyfile(file=''):
    """Runs a python file in a window of PyTools Prompt."""
    import os
    os.system('cmd.exe /f %USERPROFILE%/AppData/Local/Programs/Python/Python39/Lib/site-packages/pytools2/pytprompt.py '+file+'.py')


def PyToolsHelp(pytools_function):
    """Opens PyTools help."""
    print(f'Opening PyTools help... (function: "{pytools_function}")')
    help(pytools_function)

def Data(data=''):
    """Gets the data and stores it in server.txt."""
    def StoreData(data_):
        """base StoreData for sub-base Data. Stores info in server."""
        write("%USERPROFILE%/AppData/Local/Programs/Python/Python39/Lib/site-packages/pytools2/server", data_ + "\n", "txt")
    StoreData(data)

def ClearData():
    """Clears the data from server.txt."""
    overwrite("%USERPROFILE%/AppData/Local/Programs/Python/Python39/Lib/site-packages/pytools2/server", '', 'txt')

def Help():
    """For information, type in PyToolsHelp([pytools command]) in Python (PyTools must be imported)"""
    print('For information, type in PyToolsHelp([pytools command]) in Python (PyTools must be imported)')

def GetData():
    """Gets the data of server.txt."""
    read("%USERPROFILE%/AppData/Local/Programs/Python/Python39/Lib/site-packages/pytools2/server", "txt")

def Tk():
    """Return a tkinter.tk object."""
    try:
        import tkinter as tk
        return tk.Tk()
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')

def TkButton(text='', font='',command=''):
    """Return a tkinter.button object."""
    try:
        import tkinter as tk
        return tk.Button(text=text, font=font,command=command)
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')

def TkLabel(text='',font=''):
    """Return a tkinter.label object."""
    try:
        import tkinter as tk
        return tk.Label(text=text, font=font)
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')

def TkCheckButton():
    """Return a tkinter.checkbutton object."""
    try:
        import tkinter as tk
        return tk.Checkbutton()
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')

def TkFrame():
    """Return a tkinter.Frame object."""
    try:
        import tkinter as tk
        return tk.Frame()
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')

def TkLabelFrame():
    """Return a tkinter.Labelframe object."""
    try:
        import tkinter as tk
        return tk.LabelFrame()
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')

def TkTest():
    """Returns a tkinter._test object."""
    try:
        import tkinter as tk
        return tk._test()
    except ImportError:
        raise PyToolsError('Error: you need to install tkinter.')
    
def InstallTk():
    """Install tkinter."""
    install("tkinter-page")

def UninstallTk():
    """Uninstall tkinter."""
    uninstall("tkinter-page")

def ReinstallTk():
    """Reinstalls tkinter."""
    UninstallTk()
    InstallTk()

# this module uses a lot of tkinter, it needs tkinter to work
from pytools.__MainLib__ import CharacterMap, TofuDetector, TofuDetection, AsciiDetector, AsciiDetection # extensions
