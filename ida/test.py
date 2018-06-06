

import pexpect
from pexpect import pxssh



user = 'zmaalick'
password = 'Finlandcsc'
host = 'ida-test-stable.csc.fi'
cmd = ''

ssh_cmd = 'ssh %s@%s "%s"' % (user, host,  cmd)

child = pexpect.spawn(ssh_cmd, timeout=10)
child.expect(['password: '])
child.sendline(password)
child.close()
