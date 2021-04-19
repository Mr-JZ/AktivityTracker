from configparser import ConfigParser
import configparser
import init_config


class Config:
    def __init__(self):
        self.parser = ConfigParser()
        try:
            self.parser.read('config.ini')
        except configparser.NoSectionError:
            init_config

    def get_startup(self):
        return self.parser.getboolean('basic', 'startup')

    def get_productive(self):
        return self.parser.getint('basic', 'productive')

    def get_location(self):
        return self.parser.get('files', 'location')

    def set_startup(self, boolean):
        if(boolean):
            self.parser.set('basic', 'startup', 'true')
        else:
            self.parser.set('basic', 'startup', 'false')

        self.save_config()

    def set_productive(self, percentage):
        self.parser.set('basic', 'productive', str(percentage))
        self.save_config()

    def set_location(self, location):
        self.parser.set('files', 'location', location)
        self.save_config()

    def save_config(self):
        with open('./config.ini', 'w') as c:
            self.parser.write(c)

if __name__ == '__main__':
    print(Config().get_startup())