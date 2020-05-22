from utils.io import json_to_dict, dict_to_json


class Config:
    def __init__(self, path):
        self.path = path
        self.values = json_to_dict(path)

    def update(self):
        self.values = json_to_dict(self.path)

    def has_val(self, val_name):
        return self.values[val_name]

    def set_val(self, val_name, val):
        self.values[val_name] = val
        dict_to_json(self.path, self.values)

    def get_val(self, val_name):
        return self.values[val_name]