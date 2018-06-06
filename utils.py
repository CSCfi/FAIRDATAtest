import json
import codecs
from config.config import load_config_variables
from pexpect import pxssh
import os


# loading configuration variables
conf = load_config_variables()

user = conf['IDA_STABLE_USER']
password = conf['IDA_STABLE_PASS']
host = conf['HOST']



path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


''''
def saveJSONFile(data):
    with codecs.open(dir_path + "/test_data/" + 'metax_dataset.json', 'w', 'utf8') as f:
        f.write(json.dumps(data, sort_keys = True, ensure_ascii=False))
'''

def loadJSONFile(filename):
    dataset_json = open(dir_path + "/test_data/"  + filename).read()
    return json.loads(dataset_json)


def restart_rabbitmq():
    s = pxssh.pxssh(timeout=10)
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'sudo service rabbitmq-server restart'
        s.logfile = open('/tmp/shlog.log', 'wb')
        s.sendline(command)
        s.expect('.*assword.*',timeout=120)
        s.sendline(password)
        #pprint(s.prompt())         # match the prompt
        #pprint(s.before)     # print everything before the prompt.
        s.logout()
        print("Rabbitmq restart")

def start_rabbitmq():
    s = pxssh.pxssh(timeout=10)
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'sudo service rabbitmq-agents restart'
        s.sendline(command)
        s.expect('.*assword.*',timeout=120)
        s.sendline(password)
        #pprint(s.prompt())         # match the prompt
        #pprint(s.before)     # print everything before the prompt.
        s.logout()
        print("Rabbitmq start")


def stop_rabbitmq():
    s = pxssh.pxssh(timeout=10)
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'sudo service rabbitmq-agents restart'
        s.sendline(command)
        s.expect('.*assword.*',timeout=120)
        s.sendline(password)
        s.logout()
        print("Rabbitmq stop")


def metax_on():
    s = pxssh.pxssh()
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'sudo cp /var/ida/tests/config/config.test /var/ida/nextcloud/config/config.php'
        s.sendline(command)
        s.expect('.*assword.*', timeout=5)
        s.sendline(password)
        s.logout()
        print("Metax starts")

def metax_off():
    s = pxssh.pxssh()
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'sudo cp /var/ida/tests/config/config.master /var/ida/nextcloud/config/config.php'
        s.sendline(command)
        s.expect('.*assword.*', timeout=5)
        s.sendline(password)
        s.logout()
        print("Metax stops")



def restart_httpd():
    s = pxssh.pxssh()
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = '/root/restart-httpd'
        s.sendline(command)
        s.expect('.*assword.*',timeout=120)
        s.sendline(password)
        s.logout()
        print("httpd restart")

def delete_file(user,data):
    s = pxssh.pxssh()
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'rm /mnt/storage_vol01/ida/%s/files/%s%s' % (user, data["project"], data["pathname"])
        s.sendline(command)
        s.expect('.*assword.*',timeout=120)
        s.sendline(password)
        s.logout()
        print("Delete file")