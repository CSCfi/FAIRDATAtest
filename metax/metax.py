import requests
from config.config import load_config_variables
import time
from pprint import pprint

# loading the configuration variables
conf = load_config_variables()
URL = conf["METAX_STABLE_DATASETS_URL"]
URL_FILES = conf["METAX_STABLE_FILES_URL"]
user = conf["ETSIN_USER"]
pwd = conf["ETSIN_PASS"]
idauser = conf["METAX_STABLE_USER"]
idapass = conf["METAX_STABLE_PASS"]

# constants
TIMEOUT = 10


def create_dataset(dataset_json):
    """ Create a dataset in MetaX.
    :return: metax-id of the created dataset.
    """
    r = requests.post(URL,
                      headers={'Content-Type': 'application/json'},
                      json=dataset_json,
                      auth=(user,pwd),
                      timeout=TIMEOUT)

    return r.status_code,r.json() #return id and created?? why to return whole dataset???



def update_dataset(urn, dataset_json):

    r = requests.put(URL + '/{id}'.format(id=urn),
                     headers={
                         'Content-Type': 'application/json'
                     },
                     json=dataset_json,
                     auth=(user, pwd),
                     timeout=TIMEOUT)
    time.sleep(10)
    #print(r.json()['next_version'])
    return r.status_code,r.json()




def delete_dataset(urn):
    """ Delete a dataset from MetaX. """

    r = requests.delete(URL + '/{id}'.format(id=urn),
                        auth=(user,pwd), timeout=TIMEOUT)
    #time.sleep(40)
    return r.status_code


def get_file(id):
    """ get a file from MetaX. """

    r = requests.get(URL_FILES + '/{id}'.format(id=id),
                        auth=(idauser,idapass), timeout=TIMEOUT)
    return r.status_code
