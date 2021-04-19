import pygetwindow as gw

class VisibleWindow():
    def __init__(self):
        sheesh = None

    def test(self):
        allWindow = gw.getAllWindows()
        for window in allWindow:
            print("Windos name: " + window.title + f" is is maximised? {window.isMaximized}")
        print(gw.getActiveWindow().box)



if __name__ == "__main__":
    VisibleWindow().test()