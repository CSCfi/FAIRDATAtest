

import pexpect
from pexpect import pxssh
from pprint import pprint





def initialize_test_account(user,password,host):
    s = pxssh.pxssh(timeout=100)
    if not s.login(host, user,password):
        print("SSH session failed on login.")
        print(str(s))
    else:
        print("SSH session login successful")
        command = 'cd /var/ida/utils; sudo -u apache /var/ida/utils/initialize_test_accounts'
        s.logfile = open('/tmp/shlog.log', 'wb')
        s.sendline(command)
        s.expect('.*assword.*', timeout=5)
        s.sendline(password)
        #pprint(s.prompt())
        #pprint(s.before)
        s.logout()
        print("Data initialized")





