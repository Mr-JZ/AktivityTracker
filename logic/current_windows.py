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


def check_point_in_window(x, y, window):
    if window.box.top <= y <= window.box.bottom and window.box.left <= x <= window.box.right:
        return True
    return False


def calculate_area_of_overlapping_window(x_left, y_top, x_right, y_bottom, window):
    window_area = window.width * window.height
    x_length = x_right - x_left
    y_length = y_bottom - y_top
    active_window_overlay_area = x_length * y_length
    return active_window_overlay_area / window_area


# Checks if the windows have overlay. Is the window smaller than the
# the first window should be the expected bigger or equal one to get true
def window_overlay(active_window, compare_window):
    window_to_small_percentage = 0.2
    window_cover_percentage = 0.4

    if active_window.title == '' or compare_window.title == '':
        return False

    # Check if the active window is in the compared one and big enough
    if (active_window.left >= compare_window.left and active_window.top >= compare_window.top and
            active_window.bottom <= compare_window.bottom and active_window.right <= compare_window.right):
        active_window_area = active_window.width * active_window.height
        compare_window_area = compare_window.width * compare_window.height
        # Checked if the area is very small so you can still see the window behind good
        if active_window_area / compare_window_area > window_to_small_percentage:
            return True

    # Check if active window is bigger as the compared one
    if (compare_window.left >= active_window.left and compare_window.top >= active_window.top and
            compare_window.bottom <= active_window.bottom and compare_window.right <= active_window.right):
        return True

    # overlay in a certain percentage
    # left_top corner
    if check_point_in_window(active_window.left, active_window.top, compare_window):
        x_left = active_window.left
        y_top = active_window.top
        x_right = compare_window.right
        y_bottom = compare_window.bottom
        if active_window.bottom < compare_window.bottom:
            y_bottom = active_window.bottom
        elif active_window.right < compare_window.right:
            x_right = active_window.right
        calculate_area_of_overlapping_window(x_left, y_top,x_right, y_bottom, compare_window)
    # left_bottom corner
    elif check_point_in_window(active_window.left, active_window.bottom, compare_window):
        x_left = active_window.left
        y_top = compare_window.top
        x_right = compare_window.right
        y_bottom = active_window.bottom
        if active_window.top > compare_window.top:
            y_top = active_window.top
        elif active_window.right < compare_window.right:
            x_right = active_window.right
        calculate_area_of_overlapping_window(x_left, y_top, x_right, y_bottom, compare_window)
    # right_top corner
    elif check_point_in_window(active_window.right, active_window.top, compare_window):
        x_left = compare_window.left
        y_top = active_window.top
        x_right = active_window.right
        y_bottom = compare_window.bottom
        if active_window.bottom < compare_window.bottom:
            y_bottom = active_window.bottom
        if active_window.left > compare_window.left:
            x_left = active_window.left
        calculate_area_of_overlapping_window(x_left, y_top, x_right, y_bottom, compare_window)
    # right_bottom corner
    elif check_point_in_window(active_window.right, active_window.bottom, compare_window):
        x_left = compare_window.left
        y_top = compare_window.top
        x_right = active_window.right
        y_bottom = active_window.bottom
        if active_window.top > compare_window.top:
            y_top = active_window.top
        if active_window.left > compare_window.left:
            x_left = active_window.left
        calculate_area_of_overlapping_window(x_left, y_top, x_right, y_bottom, compare_window)
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
                current_time = datetime.datetime.now()
                duration = current_time - self.list_visible_windows[window][1]
                MainCSV().add_time(window, duration.seconds)
                self.list_visible_windows.pop(window)
                break
        if not FilterTab().filter(active_windows.title) in self.list_visible_windows:
            self.list_visible_windows[FilterTab().filter(active_windows.title)] = (active_windows, datetime.datetime.now())
        # TODO check the location of the window if the location is new update it

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
