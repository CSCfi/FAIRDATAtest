import json
import os

import requests

from config import conf_vars


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


def service_configured(service_name):
    return service_name in conf_vars and conf_vars[service_name].get('HOST', '')


def get_minimal_dataset_template(template_type='service'):
    assert template_type in ['service', 'enduser']

    if not service_configured('METAX'):
        raise Exception('Must configure Metax host in order to retrieve dataset template')

    resp = requests.get(
        'https://%s/rpc/datasets/get_minimal_dataset_template?type=%s' % (conf_vars['METAX']['HOST'], template_type),
        verify=False
    )

    if resp.status_code != 200:
        raise Exception('Error retrieving dataset template from metax: %s' % str(resp.content))

    try:
        return resp.json()
    except Exception:
        raise Exception('Error retrieving dataset template from metax: %s' % str(resp.content))


def load_json_file(filename):
    with open(dir_path + "/test_data/" + filename) as file:
        return json.load(file)
