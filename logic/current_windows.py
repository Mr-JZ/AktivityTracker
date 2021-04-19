import pygetwindow as gw
import time
import threading
from tab_filter import FilterTab


def possible_windows():
    tmp = []
    all_winows = gw.getAllWindows()
    for window in all_winows:
        if not window.isMinimized:
            tmp.append(window)
    return tmp


# locks in the list if there is a window with the same name
def window_in_list(window_dic, window):
    for tmp in window_dic:
        if tmp == FilterTab().filter(window.title):
            return True
    return False


# This is for the left upper corner sometime there not spot on of each other so you could make the tolerance bigger
def check_corner_tolerant(window_1, window_2):
    tolerant = 10
    if window_1.box.left + tolerant >= window_2.box.left >= window_1.box.left - tolerant and window_1.box.top + tolerant >= window_2.box.top >= window_1.box.top - tolerant:
        return True
    return False


# Checks if the windows have overlay. Is the window smaller than the
# the first window should be the expected bigger or equal one to get true
def window_overlay(window_1, window_2):
    if window_1.title == '' or window_2.title == '':
        return False
    if check_corner_tolerant(window_1,
                             window_2) and window_1.box.width <= window_2.box.width and window_1.box.height <= window_2.box.height:
        return True
    return False


class VisibleWindow:
    def __init__(self):
        self.list_visible_windows = {}
        self.start_algorithm()

    def start_algorithm(self):
        while True:
            self.visible_windows()
            time.sleep(1)
            print(self.list_visible_windows)

    def visible_windows(self):
        active_windows = gw.getActiveWindow()
        # print('Aktiv window: '+ active_windows.title)
        for window in self.list_visible_windows:
            # print('A Window: ' + window.title)
            print(window)
            if window_overlay(active_windows, self.list_visible_windows[window]):
                self.list_visible_windows.pop(window)
                self.list_visible_windows[FilterTab().filter(active_windows.title)] = active_windows
                return
        if window_in_list(self.list_visible_windows, active_windows):
            return

        self.list_visible_windows[FilterTab().filter(active_windows.title)] = active_windows


def threading_():
    x = threading.Thread(target=VisibleWindow, daemon=True)
    x.start()
    x.join(timeout=100)


if __name__ == "__main__":
    threading_()
    # all_window = gw.getAllWindows()
    # for i in range(len(all_window) - 1):
    #   if window_overlay(all_window[i], all_window[i + 1]):
    #      print('Windows: ' + all_window[i].title + ' and ' + all_window[i + 1].title)
    #     print(window_overlay(all_window[i], all_window[i + 1]))
