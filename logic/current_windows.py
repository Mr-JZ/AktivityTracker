import pygetwindow as gw
import datetime
import threading
import time
from tab_filter import FilterTab
from data.main_csv import MainCSV


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
        if tmp[0].title == FilterTab().filter(window.title):
            return True
    return False

def check_point_in_window(x, y , window):
    if window.box.top <= y <= window.box.bottom and window.box.left <= x <= window.box.right:
        return True
    return False

# Checks if the windows have overlay. Is the window smaller than the
# the first window should be the expected bigger or equal one to get true
def window_overlay(activ_window, compare_window):
    window_to_small_percentage = 0.2
    window_cover_percentage = 0.4

    if activ_window.title == '' or compare_window.title == '':
        return False

    # Check if the active window is in the compared one and big enough
    if (activ_window.left >= compare_window.left and activ_window.top >= compare_window.top and
        activ_window.bottom <= compare_window.bottom and activ_window.right <= compare_window.right):
        activ_window_area = activ_window.width * activ_window.height
        compare_window_area = compare_window.width * compare_window.height
        # Checked if the area is very small so you can still see the window behind good
        if activ_window_area/compare_window_area > window_to_small_percentage:
            return True

    # Check if active window is bigger as the compared one
    if (compare_window.left >= activ_window.left and compare_window.top >= activ_window.top and
            compare_window.bottom <= activ_window.bottom and compare_window.right <= activ_window.right):
        return True

    # overlay in a certain percentage
    # left_top corner
    if check_point_in_window(activ_window.left, activ_window.top, compare_window):
        None
    # left_bottom corner
    if check_point_in_window(activ_window.left, activ_window.bottom, compare_window):
        None
    # right_top corner
    if check_point_in_window(activ_window.right, activ_window.top, compare_window):
        None
    # right_bottom corner
    if check_point_in_window(activ_window.right, activ_window.bottom, compare_window):
        None
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
        if window_in_list(self.list_visible_windows, active_windows):
            return
        for window in self.list_visible_windows:
            # print('A Window: ' + window.title)
            # print(window)

            # we use the parameter active window and the dictionary with the window object
            if window_overlay(active_windows, self.list_visible_windows[window][0]):
                # TODO add the file to the .csv
                current_time = datetime.datetime.now()
                duration = current_time - self.list_visible_windows[window][1]
                MainCSV().add_time(window, duration.seconds)
                self.list_visible_windows.pop(window)
                break

        self.list_visible_windows[FilterTab().filter(active_windows.title)] = (active_windows, datetime.datetime.now())


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
