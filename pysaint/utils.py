import os
import errno
import pickle
from json import load
import json


def save_pickle(directory, file_name, python_object):
    if not os.path.exists(directory):
        try:
            os.makedirs(os.path.dirname(directory))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    if directory[-1] != '/':
        directory += '/'
    full_path = directory + file_name

    with open(full_path, "wb") as _f:
        pickle.dump(python_object, _f, protocol=pickle.HIGHEST_PROTOCOL)


def write_file(directory, file_name, content):
    if directory[-1] != '/':
        directory += '/'
    full_path = directory + file_name

    f = open(full_path, 'w')
    f.write(content)
    f.close()


def load_pickle(directory, file_name):
    if directory[-1] != '/':
        directory += '/'
    full_path = directory + file_name

    if not os.path.exists(full_path):
        raise Exception('cannot find {}'.format(full_path))

    with open(full_path, "rb") as _f:
        return pickle.load(_f)


def load_map(path='./map.json'):
    return load(open(path, 'rb'))


def dictionary_to_json(py_dict):
    """
    :param py_dict:
    python dictionary
    :return:
    serialized json string
    """
    return json.dumps(py_dict, ensure_ascii=False, indent=4)


def save_json(directory, file_name, py_dict):
    if not os.path.exists(directory):
        try:
            os.makedirs(os.path.dirname(directory))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    if directory[-1] != '/':
        directory += '/'

    json_string = dictionary_to_json(py_dict)
    write_file(directory, file_name, json_string)
