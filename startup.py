import os


class startup():
    def __init__(self):
        self.startupdirectory()

    def startupdirectory(self):
        return os.path.join(os.getenv("appdata"),"Microsoft","Windows","Start Menu","Programs","Startup")

if __name__ == "__main__":
    print(startup())
