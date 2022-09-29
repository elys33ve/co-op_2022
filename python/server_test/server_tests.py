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
from time import sleep
import iperf3, paramiko, os


#################################

"""
iperf3 -B IPADDRESS -s
iperf3 -u -B IPCLIENT -c IPSERVER -b 400m -t 600 -l 1412 -Z

ssh admin@powerstrip -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa 
uom set "relay/outlets/1/state" "false"
uom set "relay/outlets/1/state" "true"
"""

#################################

ifconfig_results = {}
#################################

def read_file (file):                   # print file contents by line to terminal (for test)
    o = open(file, 'r')
    for line in o:
        print(line)

def clear_file (file):                  # clear defult results file
    w = open(file, 'w')
    w.close()

#################################


### gets errors number results from ifconfig output and adds to dict
def ifconfig_parse (ifconfig, num='x'):
    errs = []

    while "RX errors" in ifconfig:
        idx = ifconfig.index("RX errors") + 10              # idx first error result
        ifconfig = ifconfig.replace(ifconfig[0:idx], '')        # replace everything before

        idx = ifconfig.index(" ")                       # idx next space
        errs.append(ifconfig[0:idx])                        # add everything before to list (errors number)

    if num != 'x':
        ifconfig_results.update({f"test {num}":errs})
    else:
        return errs




### append to txt file
def append_file (result_list, new_file=False, filename='test_results.txt'):
    a = open(filename, 'a')

    ### ADD LATER ALSKDJFL;SAKDJF;LSAKDJ ---- if new_file == True, and defult filename exists, create new file
    ### with defult name +1 until DNE

    for i in range(len(result_list)):           # write results to file
        a.write(f"{result_list[i]}\n")

    a.close()


### print ressults
def print_results ():
    for i in range(len(ifconfig_results)):
        print(ifconfig_results[f'test i'])



##########################################################################################3




### ssh
def ssh (command, host=board_ip, username=board_user, password=board_pass, readout=True):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command(command)

    if readout == True:
        print("_stderr = {}\n_stdout = {}".format(_stderr, _stdout))
        #output = _stdout.read().decode()

    client.close()
    return _stdout


### run server test on board
def run_server (server_ip=server_ip, readout=True):
    server_start = f'iperf3 -B {server_ip} -s'

    if board_ip == server_ip or board_data == server_ip:
        ssh(server_start, readout=readout)
    else:
        x = os.popen(server_start).read()



### run client test on pc (and wait for test to finish)
def run_client (client_ip=client_ip, server_ip=server_ip, seconds=seconds, mbps=mbps, readout=True):
    client_start = f'iperf3 -u -B {client_ip} -c {server_ip} -b {mbps}m -t {seconds} -l 1412 -Z'

    print(f"{board_ip}, {server_ip}, {board_data}, {server_ip}")
    if board_ip == client_ip or board_data == client_ip:
        ssh(client_start, readout=readout)
    else:
        x = os.popen(client_start).read()



### turn on power (and wait for board to boot)
def power_cycle (do=2, outlet=outlet):                             # 0=off, 1=on, 2=reset (off/on)
    OFF = f'uom set "relay/outlets/{outlet}/state" "false"'
    ON = f'uom set "relay/outlets/{outlet}/state" "true"'
    if do == 0:         # turn off
        ssh(OFF, power_ip, power_user, power_pass)
    elif do == 1:       # turn on
        ssh(ON, power_ip, power_user, power_pass)
    else:               # reset (off/on)
        ssh(OFF, power_ip, power_user, power_pass)
        ssh(ON, power_ip, power_user, power_pass)    



### wait for board to boot up after power on
def wait_start ():
    sleep(10)


### run ifconfig on board (and get temp txt file of results)
def get_ifconfig ():
    ifconfig = os.popen("ifconfig").read()
    return ifconfig
