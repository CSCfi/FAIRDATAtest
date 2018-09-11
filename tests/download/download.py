import requests

from config import conf_vars


try:
    download_host = conf_vars['DOWNLOAD']['HOST']
    download_dataset_url = 'https://%s/api/v1/dataset/' % download_host
except Exception as e:
    print('Note: Download not running')


def download_dataset(urn):
    '''
    Download a dataset or file or dir in Download.
    '''
    r = requests.get(download_dataset_url + urn, verify=False)
    return r.status_code, r.content
