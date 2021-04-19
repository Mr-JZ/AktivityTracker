import re
from data.main_data import Data


class FilterTab:
    def __init__(self):
        self.programs = Data().get_programs()

    def filter(self, text):
        for program in self.programs:
            if program in text:
                return program
        return text
