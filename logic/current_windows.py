import win32gui
import win32api
import win32process

import pygetwindow as gw

class VisibleWindow():
    def __init__(self):
        sheesh = None

    def getwindows(self):
        # this is the activ window
        # print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        # macht nichts
        print(win32gui.GetWindowText(win32gui.GetActiveWindow()))

    def pygetwindow(self):
        # you get every window that is current open
        # print(gw.getAllWindows())
        print(win32gui.GetDesktopWindow())

    def test(self):
        allWindow = gw.getAllWindows()
        for window in allWindow:
            print("Windos name: " + window.title + f" is is maximised? {window.isMaximized}")
        print(gw.getActiveWindow().box)



if __name__ == "__main__":
    VisibleWindow().test()