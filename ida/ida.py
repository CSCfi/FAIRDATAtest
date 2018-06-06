import requests
from config.config import load_config_variables


# loading the configuration variables
conf = load_config_variables()

URL = conf['IDA_API_ROOT_URL']
PASS = conf['PROJ_USER_PASS']
    
# constants
TIMEOUT = 30


def freeze_file(USER,data):
    """ freeze a file.
    :return: status code, response data
    """
    r = requests.post('%s/freeze' % URL, json=data, auth=(USER,PASS),verify = False)
    return r.status_code, r.json()

def unfreeze_file(USER,data):
    """ unfreeze a file.
    :return: status code, response data
    """
    r = requests.post('%s/unfreeze' % URL, json=data, auth=(USER,PASS),verify = False)
    return r.status_code, r.json()

def delete_file(USER,data):
    """ delete frozen file.
    :return: status code
    """
    r = requests.post('%s/delete' % URL, json=data, auth=(USER,PASS),verify = False)
    return r.status_code


def get_frozen_node(USER, data,pname):
    """ retrieve frozen node data
    :return: status code, response data
    """
    r = requests.get('%s/files/byProjectPathname/%s' % (URL,pname), json=data, auth=(USER,PASS),verify = False)
    return r.status_code, r.json()

def get_frozen_node_action(USER,pid):
    """ retrieve frozen node data associated with action
    :return: status code, response data
    """
    r = requests.get('%s/files/action/%s' % (URL,pid),auth=(USER,PASS),verify = False)
    return r.status_code, r.json()

def get_node_details(USER,pid):
    """ retrieve frozen node details
    :return: status code, response data
    """
    r = requests.get('%s/files/%s' % (URL,pid),auth=(USER,PASS),verify = False)
    return r.status_code, r.json()

def get_actions(USER,data):
    """ retrieve list of all the actions by their status
    :return: status code, response data
    """
    r = requests.get('%s/actions' %URL, json=data, auth=(USER,PASS),verify=False)
    return r.status_code, r.json()


def get_specific_actions(USER,data,pid):
    """ retrieve specific action of specific status
    :return: status code, response data
    """
    r = requests.get('%s/actions/%s' %(URL,pid), json=data, auth=(USER,PASS),verify=False)
    return r.status_code, r.json()


def update_node_details(USER,pid,data):
    """ Update any specific node node 
    :return: status code, response data
    """
    r = requests.post('%s/files/%s' % (URL,pid), json=data, auth=(USER,PASS),verify = False)
    return r.status_code

def update_action_details(USER,pid,data):
    """ update any specific action
    :return: status code, response data
    """
    r = requests.post('%s/actions/%s' % (URL,pid), json=data, auth=(USER,PASS),verify = False)
    return r.status_code



