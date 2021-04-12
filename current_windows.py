import win32gui
import win32process

def topLevelWindows(pid):

    def enumHandler(hwnd, data):
        if win32process.GetWindowThreadProcessId(hwnd)[1] == pid:
            windows.append(hwnd)
        return True

    windows = []
    win32gui.EnumWindows(enumHandler, 0)
    return windows

for hwnd in topLevelWindows(pid):
    if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd):
        print('%.8x %s' % (hwnd, win32gui.GetWindowText(hwnd)))