import requests

from config.config import load_config_variables

# loading the configuration variables
conf = load_config_variables()
HOST = conf["ETSIN_HOST"]
user = conf["ETSIN_USER"]
pwd = conf["ETSIN_PASS"]

# constants
TIMEOUT = 30

URL = "https://%s/es/metax/dataset/" % HOST


def view_dataset(urn):
    """ View a dataset in Etsin.
    :return: metax-id of the created dataset.
    """
    r = requests.get(URL + urn, auth=(user, pwd), verify=False)
    return r.status_code, r.json()
