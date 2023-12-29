import json

class JSONManager:
    def __init__(self) -> None:
        pass

    def read_data(self, filename) -> list:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data

    def write_data(self, filename, data):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)