import requests

from config import conf_vars


try:
    etsin_host = conf_vars['ETSIN']['HOST']
    etsin_dataset_url = 'https://%s/es/metax/dataset/' % etsin_host
except Exception as e:
    print('Note: Etsin not configured')


def view_dataset(urn):
    '''
    View a dataset in Etsin.
    '''
    r = requests.get(etsin_dataset_url + urn, verify=False)
    return r.status_code, r.json()
