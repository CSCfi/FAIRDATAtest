import requests
import os

from config import conf_vars


try:
    HOST = conf_vars["QVAIN"]["HOST"]
    URL = "https://%s/api/datasets/" % HOST
except:
    print('Note: Qvain not configured')

TIMEOUT = 10
SID = os.environ.get('QVAIN_SID') or conf_vars['QVAIN']['SID']
if not SID:
    raise Exception("qvain: session id `SID` unset")


def create_dataset(dataset):
    '''
    create_dataset creates a new Qvain dataset.

    :return: status, json
    '''
    r = requests.post(URL,
                      cookies={'sid': SID},
                      json=dataset,
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def update_dataset(dataset_id, dataset):
    '''
    update_dataset updates an existing dataset by id.

    Note that the API responds with 204 No Content on success,
    so this function doesn't return json.

    :return: status, response
    '''
    r = requests.put(URL + dataset_id,
                     cookies={'sid': SID},
                     json=dataset,
                     timeout=TIMEOUT)

    return r.status_code, r


def get_dataset(dataset_id):
    '''
    get_dataset gets a dataset from Qvain by id.
    
    :return: status, json
    '''
    r = requests.get(URL + dataset_id,
                     cookies={'sid': SID},
                     timeout=TIMEOUT)
    return r.status_code, r.json()


def publish_dataset(dataset_id):
    '''
    publish_dataset publishes a Qvain dataset to Metax.

    :return: status, json
    '''
    r = requests.get(URL + dataset_id + '/publish',
                      cookies={'sid': SID},
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def list_datasets():
    '''
    list_datasets lists a user's datasets.

    :return: status, json
    '''
    r = requests.get(URL,
                      cookies={'sid': SID},
                      timeout=TIMEOUT)

    return r.status_code, r.json()


def sync_datasets():
    '''
    sync_datasets lists a user's datasets but triggers a synchronisation with the Metax API first.

    :return: status, json
    '''
    r = requests.get(URL + '?fetch',
                      cookies={'sid': SID},
                      timeout=TIMEOUT)

    return r.status_code, r.json()



def make_dataset_from(fairdata_dataset):
    '''
    make_dataset_from creates a dataset based on a fairdata (metax) dataset.

    This throws away everything except 'research_dataset' because Qvain
    will wrap the data in the appropriate template for the specified schema.

    Qvain groups structurally congruent (interchangable) datasets in "families";
    Fairdata IDA and PAS schemas have type 2 (int).

    Qvain refers to the current Metax schema as "metax-ida".

    :return: object that parses to JSON for Qvain API
    '''
    if not 'research_dataset' in fairdata_dataset:
        raise Exception("no 'research_dataset' field in test dataset")

    return {
        'valid': False,
        'type': 2,
        'schema': 'metax-ida',
        'dataset': fairdata_dataset['research_dataset'],
    }
