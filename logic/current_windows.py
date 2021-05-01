import pygetwindow as gw
import datetime
import threading
import time
from tab_filter import FilterTab
from data.main_csv import MainCSV


def possible_windows():
    tmp = []
    all_windows = gw.getAllWindows()
    for window in all_windows:
        if not window.isMinimized:
            tmp.append(window)
    return tmp


# locks in the list if there is a window with the same name
def window_in_list(window_dic, window):
    for tmp in window_dic:
        if tmp == window._hWnd:
            return True
    return False


def check_point_in_window(x, y, window):
    if window.top <= y <= window.bottom and window.left <= x <= window.right:
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

    if active_window._hWnd == '' or compare_window._hWnd == '':
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
        calculate_area_of_overlapping_window(x_left, y_top, x_right, y_bottom, compare_window)
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
            time.sleep(2)
            print(self.readable_name())

    def visible_windows(self):
        # print('activated')
        active_windows = gw.getActiveWindow()
        # print('Aktiv window: '+ active_windows._hWnd
        if window_in_list(self.list_visible_windows, active_windows):
            old_active_window_name = active_windows._hWnd
            old_active_window = self.list_visible_windows[old_active_window_name][0]
            if old_active_window.box != active_windows.box:
                print('update geometry')
                self.list_visible_windows[old_active_window_name][0] = active_windows
        for window in self.list_visible_windows:
            # print('A Window: ' + window._hWnd
            # print(window)
            # print('look through the windows')
            # we use the parameter active window and the dictionary with the window object
            if window_overlay(active_windows, self.list_visible_windows[window][0]):
                current_time = datetime.datetime.now()
                duration = current_time - self.list_visible_windows[window][1]
                MainCSV().add_time(FilterTab().filter(self.list_visible_windows[window][0].title), duration.seconds)
                self.list_visible_windows.pop(window)
                break
        if not (active_windows._hWnd in self.list_visible_windows):
            self.list_visible_windows[active_windows._hWnd] = (
                active_windows, datetime.datetime.now())

    def readable_name(self):
        tmp_dic = {}
        for tmp in self.list_visible_windows:
            tmp_dic[self.list_visible_windows[tmp][0].title] = self.list_visible_windows[tmp][0].box
        return tmp_dic


def threading_():
    x = threading.Thread(target=VisibleWindow, daemon=True)
    x.start()
    x.join(timeout=100)


if __name__ == "__main__":
    threading_()
    # all_window = gw.getAllWindows()
    # for i in range(len(all_window) - 1):
    #   if window_overlay(all_window[i], all_window[i + 1]):
    #      print('Windows: ' + all_window[i]._hWnd+ ' and ' + all_window[i + 1]._hWnd
    #     print(window_overlay(all_window[i], all_window[i + 1]))
