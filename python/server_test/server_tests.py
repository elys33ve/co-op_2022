# python scripts for conducting multiple tests and getting results for number of errors each trial
"""
this script is function defs for the command line stuff
    - turn on power (and wait for board to boot)
    - ssh into board
    - run server test on board
    - run client test on pc (and wait for test to finish)
    - run ifconfig on board (and get temp txt file of results)
"""

from server_test_info import *
import iperf3, paramiko, os

#################################



#################################


### ssh
def ssh (command, host=board_ip, username=board_user, password=board_pass):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command(command)

    output = _stdout.read().decode()

    client.close()
    return output



### turn on power (and wait for board to boot)
def power_cycle (do=2):                             # 0=off, 1=on, 2=reset (off/on)
    OFF = 'uom set "relay/outlets/1/state" "false"'
    ON = 'uom set "relay/outlets/1/state" "true"'
    
    if do == 0:         # turn off
        ssh(OFF, power_ip, power_user, power_pass)
    elif do == 1:       # turn on
        ssh(ON, power_ip, power_user, power_pass)
    else:               # reset (off/on)
        ssh(OFF, power_ip, power_user, power_pass)
        ssh(ON, power_ip, power_user, power_pass)    

### run server test on board
def run_server ():
    server = iperf3.Server()
    server.bind_address = server_ip
    server.port = port
    server.verbose = False

    while True:
        server.run()


### run client test on pc (and wait for test to finish)
def run_client ():
    client = iperf3.Client()
    client.server_hostname = client_ip
    client.port = port
    client.json_output = False
    result = client.run()


### run ifconfig on board (and get temp txt file of results)
def get_ifconfig ():
    ifconfig = os.popen("ifconfig").read()
    return ifconfig
