import requests

from config import conf_vars


requests.packages.urllib3.disable_warnings()

try:
    HOST = conf_vars['PAS']['HOST']
    USER = conf_vars['PAS']['USERS']['PAS']['USER']
    PASS = conf_vars['PAS']['USERS']['PAS']['PASS']
    user = (USER, PASS)
    URL = 'https://%s/secure/api/1.0/' % HOST
except Exception as e:
    print('Note: PAS not configured')


def preserve_dataset(id):
    """ preserve a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/preserve' % (URL, id), auth=user, verify=False)
    return r.status_code


def reject_dataset(id):
    """ reject a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/reject' % (URL, id), auth=user, verify=False)
    return r.status_code


def remove_dataset(id):
    """ remove a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/remove' % (URL, id), auth=user, verify=False)
    return r.status_code


def reset_dataset(id):
    """ reset a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/reset' % (URL, id), auth=user, verify=False)
    return r.status_code
