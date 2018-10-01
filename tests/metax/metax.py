import time

import requests

from config import conf_vars


try:
    metax_host = conf_vars["METAX"]['HOST']
    datasetuser = conf_vars["METAX"]['USERS']['ETSIN']['USER']
    datasetpwd = conf_vars["METAX"]['USERS']['ETSIN']['PASS']
    fileuser = conf_vars["METAX"]['USERS']['IDA']['USER']
    filepwd = conf_vars["METAX"]['USERS']['IDA']['PASS']
    URL_datasets = "https://%s/rest/datasets" % metax_host
    URL_files = "https://%s/rest/files" % metax_host
except Exception as e:
    print('Note: Metax not configured (requires users: etsin, ida)')

# constants
TIMEOUT = 10


def create_dataset(dataset_json):
    """ Create a dataset in MetaX.
    :return: metax-id of the created dataset.
    """
    resp = requests.post(URL_datasets,
                      headers={'Content-Type': 'application/json'},
                      json=dataset_json,
                      auth=(datasetuser, datasetpwd),
                      timeout=TIMEOUT,
                      verify=False)
    return resp.status_code, resp.json()


def update_dataset(urn, dataset_json):
    r = requests.put(URL_datasets + '/{id}'.format(id=urn),
                     headers={ 'Content-Type': 'application/json' },
                     json=dataset_json,
                     auth=(datasetuser, datasetpwd),
                     timeout=TIMEOUT,
                     verify=False)
    time.sleep(10)
    # print(r.json()['next_version'])
    return r.status_code, r.json()


def delete_dataset(urn):
    """ Delete a dataset from MetaX. """

    r = requests.delete(URL_datasets + '/{id}'.format(id=urn),
                        auth=(datasetuser, datasetpwd), timeout=TIMEOUT,
                        verify=False)
    # time.sleep(40)
    return r.status_code


def get_file(id):
    """ get a file from MetaX. """

    r = requests.get(URL_files + '/{id}'.format(id=id),
                     auth=(fileuser, filepwd), timeout=TIMEOUT,
                     verify=False)
    return r.status_code


def find_file_by_project_and_path(project, file_path):
    resp = requests.get('%s?project_identifier=%s&no_paging=true&fields=file_path' % (URL_files, project),
        auth=(fileuser, filepwd), timeout=TIMEOUT, verify=False)
    if resp.status_code == 200:
        for file in resp.json()['results']:
            if file['file_path'].startswith(file_path):
                return True
    return False


def flush_project(pname):
    """ flush all the files related to particular project """

    resp = requests.post(URL_files + '/flush_project?project=%s' % pname,
                      auth=(fileuser, filepwd), timeout=TIMEOUT,
                      verify=False)
    if resp.status_code not in (200, 204):
        print('Warning: Metax failed to flush project %s. Reason: %s' % (pname, str(resp.content)))
    return resp.status_code
