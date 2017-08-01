import os
import pexpect
import sys

size=len(sys.argv)
passphrase=sys.argv[size-1]
passphrase.strip(' ')
ssid=sys.argv[1]
if size>=4:
    i=size-2
    for loop in range(1,i):
        ssid=ssid+' '+sys.argv[loop+1]
        print ssid

cmd_arg=', '.join(sys.argv[1:])
print cmd_arg
connmanctl=pexpect.spawn('connmanctl')
connmanctl.expect('connmanctl>')
connmanctl.sendline('agent on')
err=connmanctl.expect(['Agent registered', 'Error'])
if err == 1:
    print 'Error in agent on'
f=open('output.txt','r')
out=f.read()
ssid_var=''
for row in out.split('\n'):
    if ssid in row:
        print row
        ssid_var=row.split()
        l=len(ssid_var)
        ssid_var[l-1].strip(' \t\r\n')

if ssid_var == '':
    print 'SSID information incorrect'
    quit()

wifi_addr='connect '+ssid_var[l-1]
print wifi_addr
connmanctl.sendline(wifi_addr)
err=connmanctl.expect(['Passphrase?','Error'])
if err == 1:
    print connmanctl.before
    print 'Error in connecting to wifi'
    quit()
connmanctl.sendline(passphrase)
connect_str='Connected ' + ssid_var[l-1]
connmanctl.expect(connect_str)
print 'wifi connected'
connmanctl.sendline('quit')
