import requests

from config.config import load_config_variables

# loading the configuration variables
conf = load_config_variables()

HOST = conf["QUVAIN_HOST"]
user = conf["QUVAIN_USER"]
pwd = conf["QUVAIN_PASS"]

TIMEOUT = 10

URL = "https://%s/api/dataset" % HOST


def create_dataset():
    """ creates a dataset in quvain
    :return: function returns status
    """
    r = requests.post(URL,
                      headers={'Authorization': 'TOK:<MY_TOKEN>'},
                      json=dataset_json,
                      auth=(user, pwd),
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def update_dataset():
    """ Update the dataset in quvain
    :return: function returns status
    """

    r = requests.post(URL,
                      headers={'Authorization': 'TOK:<MY_TOKEN>'},
                      json=dataset_json,
                      auth=(user, pwd),
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def sync_dataset():
    """ Sync the metax datasets with quvain
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
