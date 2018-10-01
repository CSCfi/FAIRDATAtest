import requests
import time

from pexpect import pxssh

from tests.metax import metax
from config import conf_vars


requests.packages.urllib3.disable_warnings()

try:
    ida_host = conf_vars['IDA']['HOST']
    ida_api_pass = conf_vars['IDA']['PROJ_USER_PASS']
    ida_api_url = "https://%s/apps/ida/api" % ida_host
    ssh_user = conf_vars['IDA']['USERS']['SSH_USER']['USER']
    ssh_password = conf_vars['IDA']['USERS']['SSH_USER']['PASS']
except Exception as e:
    print('Note: Ida not configured')


'''
Note: In this file, the 'user' comes as a parameter, but the password
just so happens to be the same for all test project-users in ida-stable.
'''


def initialize_test_accounts():
    print('Initializing ida test accounts...')
    s = pxssh.pxssh(timeout=100)
    if not s.login(ida_host, ssh_user, ssh_password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'cd /var/ida/utils; sudo -u apache /var/ida/utils/initialize_test_accounts'
        s.logfile = open('/tmp/shlog.log', 'wb')
        s.sendline(command)
        s.expect('.*assword.*', timeout=5)
        s.sendline(ssh_password)
        # pprint(s.prompt())
        # pprint(s.before)
        s.logout()
        print("Data initialized")


def wait_until_file_appears_in_metax(project, file_path, timeout=30):
    """
    When freezing files, it takes a while for a file to appear in metax.
    """
    print('Waiting until file appears in metax...')
    for i in range(0, timeout):
        if metax.find_file_by_project_and_path(project, file_path):
            print('Found the file!')
            return True
        time.sleep(1)
        if i % 5 == 0 and i > 0:
            print('Still didnt find...')
    return False


def wait_until_file_disappears_from_metax(project, file_path, timeout=30):
    """
    When unfreezing/deleting files, it takes a while for a file to be removed from metax.
    """
    print('Waiting until file disappears from metax...')
    for i in range(0, timeout):
        if not metax.find_file_by_project_and_path(project, file_path):
            print('File is gone!')
            return True
        time.sleep(1)
        if i % 5 == 0 and i > 0:
            print('File still not gone...')
    return False


def freeze_file(user, data):
    """ freeze a file.
    :return: status code, response data
    """
    r = requests.post('%s/freeze' % ida_api_url, json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def unfreeze_file(user, data):
    """ unfreeze a file.
    :return: status code, response data
    """
    r = requests.post('%s/unfreeze' % ida_api_url, json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def delete_file(user, data):
    """ delete frozen file.
    :return: status code
    """
    r = requests.post('%s/delete' % ida_api_url, json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code


def get_frozen_node(user, data, pname):
    """ retrieve frozen node data
    :return: status code, response data
    """
    r = requests.get('%s/files/byProjectPathname/%s' % (ida_api_url, pname), json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def get_frozen_node_action(user, pid):
    """ retrieve frozen node data associated with action
    :return: status code, response data
    """
    r = requests.get('%s/files/action/%s' % (ida_api_url, pid), auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def get_node_details(user, pid):
    """ retrieve frozen node details
    :return: status code, response data
    """
    r = requests.get('%s/files/%s' % (ida_api_url, pid), auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def get_actions(user, data):
    """ retrieve list of all the actions by their status
    :return: status code, response data
    """
    r = requests.get('%s/actions' % ida_api_url, json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def get_specific_actions(user, data, pid):
    """ retrieve specific action of specific status
    :return: status code, response data
    """
    r = requests.get('%s/actions/%s' % (ida_api_url, pid), json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code, r.json()


def update_node_details(user, pid, data):
    """ Update any specific node node
    :return: status code, response data
    """
    r = requests.post('%s/files/%s' % (ida_api_url, pid), json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code


def update_action_details(user, pid, data):
    """ update any specific action
    :return: status code, response data
    """
    r = requests.post('%s/actions/%s' % (ida_api_url, pid), json=data, auth=(user, ida_api_pass), verify=False)
    return r.status_code
