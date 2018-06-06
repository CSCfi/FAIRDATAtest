import requests
from config.config import load_config_variables


# loading the configuration variables
conf = load_config_variables()


URL = conf['DPRES_URL']
USER = conf['DPRES_USER']
PASS = conf['DPRES_PASS']
user = (USER, PASS)
    
# constants
TIMEOUT = 30


def preserve_dataset(id):
    """ preserve a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/preserve' % (URL,id), auth=user, verify=False)
    return r.status_code


def reject_dataset(id):
    """ reject a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/reject' % (URL,id), auth=user, verify=False)
    return r.status_code


def remove_dataset(id):
    """ remove a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/remove' % (URL,id), auth=user, verify=False)
    return r.status_code


def reset_dataset(id):
    """ reset a dataset in dpres.
    :return: status code
    """
    r = requests.post('%s/datasets/%s/resetd' % (URL,id), auth=user, verify=False)
    return r.status_code
