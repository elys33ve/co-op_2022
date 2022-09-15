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
from paramiko import SSHClient
import os
import iperf3


#################################

#################################


### turn on power (and wait for board to boot)
def power_on ():
    return 0

### ssh into board
def ssh (command, server_ip=server_ip, username=username, password=password):
    ssh = SSHClient
    ssh.connect(server_ip, username=username, password=password)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

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
