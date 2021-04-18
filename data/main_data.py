import json

class Data():
    def __init__(self):
        self.no_data = False
        try:
            with open('./data.json') as file:
                self.data = json.load(file)
        except FileNotFoundError or json.decoder.JSONDecodeError:
            with open('./data.json', 'w') as file:
                file.write('')
            self.no_data = True

if __name__ == '__main__':
    Data()