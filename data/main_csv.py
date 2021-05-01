import pandas as pd


class MainCSV:
    def __init__(self):
        # is that clean?
        self.data_location = './main.csv'
        try:
            try:
                with open(self.data_location, 'r') as file:
                    self.data = pd.read_csv(file, delimiter=',')
            except pd.errors.EmptyDataError:
                self.create_new_data()
        except FileNotFoundError:
            self.create_new_data()

    def create_new_data(self):
        data = {'Zoom': []}
        self.data = pd.DataFrame(data)
        self.save_data()

    def add_time(self, window_name, duration):
        try:
            is_null_list = self.data[self.data[window_name].isnull()].index.tolist()
        except KeyError:
            is_null_list = [0]
        try:
            self.data.loc[is_null_list[0], window_name] = duration
        except IndexError:
            self.data.loc[self.data.size - 1, window_name] = duration
        self.save_data()

    def save_data(self):
        self.data.to_csv(self.data_location, index=False)


if __name__ == '__main__':
    print(MainCSV().add_time('Zoom', 2342))
