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
from time import sleep, time
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

##########################################################################################3


### ssh
def ssh (command, host=board_ip, username=board_user, password=board_pass, readout=True):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command(command)

    if readout == True:                                         # return the iperf3 stuff
        output = f"_stderr = {_stderr}\n_stdout = {_stdout}"
        #print(output)
        output = _stdout
    else:                                                       # return normal commands
        output = _stdout.read().decode()

    client.close()

    return output


### run server test
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


### if server running on board, ssh and kill process
def kill_server ():
    grep = ssh("ps aux | grep iperf")

    if 'iperf3' in grep:
        ssh("pkill iperf3")




#################################




### run ifconfig on board (and get temp txt file of results)
def show_ifconfig ():
    #ifconfig = os.popen("ifconfig").read()     # pc
    ifconfig = ssh("ifconfig", readout=False)   # board
    return ifconfig


### get info from ifconfig string
def get_info (term):
    ifconfig = ssh("ifconfig", readout=False)
    errs = []

    while term in ifconfig:
        idx = ifconfig.index(term) + len(term)+1              # idx first error result
        ifconfig = ifconfig.replace(ifconfig[0:idx], '')        # replace everything before

        idx = ifconfig.index(" ")                       # idx next space
        errs.append(ifconfig[0:idx])                        # add everything before to list (errors number)

    return errs


### gets errors number results from ifconfig output and adds to dict
def ifconfig_parse (num='x'):
    
    rxp = get_info("RX packets")
    rxe = get_info("RX errors")
    #rovr = get_info("overruns")

    txp = get_info("TX packets")
    txe = get_info("TX errors")
    #tovr = get_info("overruns")
    
    ifconfig_results[num] = [rxp, rxe, txp, txe]



### print and format info from ifconfig
def print_info ():
    err = ["RX packets", "RX errors", "TX packets", "TX errors"]
    keys = list(ifconfig_results)

    for i in range(len(ifconfig_results)):
        print(f"\n{keys[i]}")
        for j in range(len(ifconfig_results[keys[i]])):
            print(f"\t{err[j]}: {ifconfig_results[keys[i]][j]}")



#################################





def test1 (seconds=seconds):

    for i in range(num_tests):
        print(f"power cycle...\n")
        power_cycle()       # takes about 5 seconds
        sleep(20)           # takes about 25 seconds to boot (but times out at 20)

        print("starting server...\n")
        run_server()                # start server

        print(f"\nrunning test {i+1} of {num_tests}")
        print(f"server = {server_ip}\tclient = {client_ip}")
        print(f"test time = {seconds} seconds\n")
        run_client(seconds=60)      # connect to server
       
        print(f"\ntest {i+1} complete.\n")  

        ifconfig_parse(i+1)

    print_info()
