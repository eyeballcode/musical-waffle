import os
import json


def exists(file):
    return os.path.exists(file)


def create_if_not_exist(file, filetype=''):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            if filetype == 'json':
                f.write('{}')
            f.close()


def read_all(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = f.readlines()
            return '\n'.join(data)
    return None


def write(file, data):
    with open(file, 'w') as f:
        f.write(data)
        f.close()


def append(file, data):
    create_if_not_exist(file)
    with open(file, 'a') as f:
        f.write(data)
        f.close()


def read_json(file):
    data = read_all(file)
    return json.loads(data)


def write_json(file, jsondata):
    data = json.dumps(jsondata)
    write(file, data)
