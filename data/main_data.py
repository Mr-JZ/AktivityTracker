import json


class Data():
    def __init__(self):
        self.no_data = False
        try:
            self.data = self.open_file()
        except FileNotFoundError:
            self.save_file()
            self.data = self.open_file()
            self.no_data = True

    def open_file(self):
        with open('./data.json') as file:
            data = json.load(file)
        return data

    def save_file(self):
        try:
            with open('./data.json', 'w') as file:
                json.dump(self.data, file)
        except AttributeError:
            with open('./data.json', 'w') as file:
                json.dump(self.init_data(), file)

    def init_data(self):
        data = {
            'browser_time': 0,
            'topics': ['unproductive', 'productive'],
            'use_since_install': 0,
            'programs': ["Word", "PowerPoint", "Excel", "Notion", "Chrome", "Edge", "Firefox", "Terminal", "Zoom",
                         "Discord", "Teams", "Spotify"]
        }
        return data

    def get_browserTime(self):
        return self.data['browser_time']

    def get_useSinceInstall(self):
        return self.data['use_since_install']

    def get_topics(self):
        return self.data['topics']

    def get_programs(self):
        return self.data['programs']

    def add_topic(self, topic):
        self.addListItem(self.data['topics'], topic)
        self.save_file()

    def set_browserTime(self, time):
        self.data['browser_time'] = time
        self.save_file()

    def set_useSinceInstall(self, time):
        self.data['use_since_install'] = time
        self.save_file()

    def add_program(self, program):
        self.addListItem(self.data['programs'], program)
        self.save_file()

    def addListItem(self, list, item):
        for i in list:
            if i == item:
                return
        list.append(item)
if __name__ == '__main__':
    print(Data().get_browserTime())
