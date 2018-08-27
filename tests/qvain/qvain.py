import requests

from config import conf_vars
from utils import load_json_file


try:
    HOST = conf_vars["QVAIN"]["HOST"]
    user = conf_vars["QVAIN"]["USERS"]["QVAIN"]["USER"]
    pwd = conf_vars["QVAIN"]["USERS"]["QVAIN"]["PASS"]
    URL = "https://%s/api/dataset" % HOST
except:
    print('Note: Qvain not configured')

TIMEOUT = 10


dataset_json = load_json_file('basic_dataset.json')


def create_dataset():
    """ creates a dataset in qvain
    :return: function returns status
    """
    r = requests.post(URL,
                      headers={'Authorization': 'TOK:<MY_TOKEN>'},
                      json=dataset_json,
                      auth=(user, pwd),
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def update_dataset():
    """ Update the dataset in qvain
    :return: function returns status
    """

    r = requests.post(URL,
                      headers={'Authorization': 'TOK:<MY_TOKEN>'},
                      json=dataset_json,
                      auth=(user, pwd),
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def sync_dataset():
    """ Sync the metax datasets with qvain
    :return: function returns status
    """

    r = requests.post(URL,
                      headers={'Authorization': 'TOK:<MY_TOKEN>'},
                      json=dataset_json,
                      auth=(user, pwd),
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def publish_dataset():
    """ Publishes the dataset to metax
    :return: function returns status
    """

    r = requests.post(URL,
                      headers={'Authorization': 'TOK:<MY_TOKEN>'},
                      json=dataset_json,
                      auth=(user, pwd),
                      timeout=TIMEOUT)

    return r.status_code, r.json()
