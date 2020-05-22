import json


def text_file_to_list(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def list_to_text_file(filename, string_list):
    with open(filename, 'w') as text_file:
        for line in string_list:
            text_file.write(f'{line}\n')


def json_to_dict(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def dict_to_json(filename, dictionary):
    with open(filename, 'w') as json_file:
        json.dump(dictionary, json_file)
