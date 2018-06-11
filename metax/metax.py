import requests
from config.config import load_config_variables
import time
from pprint import pprint

# loading the configuration variables
conf = load_config_variables()

HOST = conf["METAX_HOST"]
datasetuser = conf["ETSIN_USER"]
datasetpwd = conf["ETSIN_PASS"]
fileuser = conf["METAX_USER"]
filepwd = conf["METAX_PASS"]

# constants
TIMEOUT = 10

URL_datasets = "https://%s/rest/datasets"%HOST
URL_files = "https://%s/rest/files"%HOST




def create_dataset(dataset_json):
    """ Create a dataset in MetaX.
    :return: metax-id of the created dataset.
    """

   
    r = requests.post(URL_datasets,
                      headers={'Content-Type': 'application/json'},
                      json=dataset_json,
                      auth=(datasetuser,datasetpwd),
                      timeout=TIMEOUT)

    return r.status_code,r.json() #return id and created?? why to return whole dataset???



def update_dataset(urn, dataset_json):

    r = requests.put(URL_datasets + '/{id}'.format(id=urn),
                     headers={
                         'Content-Type': 'application/json'
                     },
                     json=dataset_json,
                     auth=(datasetuser, datasetpwd),
                     timeout=TIMEOUT)
    time.sleep(10)
    #print(r.json()['next_version'])
    return r.status_code,r.json()




def delete_dataset(urn):
    """ Delete a dataset from MetaX. """

    r = requests.delete(URL_datasets + '/{id}'.format(id=urn),
                        auth=(datasetuser,datasetpwd), timeout=TIMEOUT)
    #time.sleep(40)
    return r.status_code


def get_file(id):
    """ get a file from MetaX. """

    r = requests.get(URL_files + '/{id}'.format(id=id),
                        auth=(fileuser,filepwd), timeout=TIMEOUT)
    return r.status_code


def flush_project(pname):
    """ flush all the files related to perticular project """

    r = requests.post(URL_files + '/flush_project?project=Project_C',
                        auth=(fileuser,filepwd), timeout=TIMEOUT)
    return r.status_code
