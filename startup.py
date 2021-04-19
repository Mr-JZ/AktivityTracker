import os

import winshell


class startup():
    def __init__(self):
        self.startupdirectory()

    def startupdirectory(self):
        return winshell.startup()

if __name__ == "__main__":
    print(startup())
    with open(os.path.join(winshell.startup(), 'test.py'), 'w') as file:
        file.write('import test ')
