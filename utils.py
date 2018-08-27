import json
import os

from config import conf_vars


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


def service_configured(service_name):
    return service_name in conf_vars and conf_vars[service_name].get('HOST', '')


def load_json_file(filename):
    with open(dir_path + "/test_data/" + filename) as file:
        return json.load(file)
