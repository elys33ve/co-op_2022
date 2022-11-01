# python scripts for conducting multiple tests and getting results for number of errors each trial
# needs to:
#   - turn on power
#   - wait for board to boot
#   - ssh into board 1 and start server
#   - ssh into baord 2 and connect to server for test
#   - wait for client to finish test
#   - run ifconfig on board
#   - write ifconfig results to txt file

import os
from time import sleep
from iperf3py_info import *          # command line stuff

#################################
ssh_server = SSH(host=board_ip1, username='alarm', password='alarm')
ssh_client = SSH(host=board_ip2, username='alarm', password='alarm')
ssh_powerswitch = SSH(host=power_ip, username='admin', password='1234')
#################################                               --- strings and file stuff
header = f"""================================
number of tests: {num_tests}
seconds per test: {seconds}
mbps: {mbps}
server ip: {server_ip}
client ip: {client_ip}
================================\n
"""

### get the four lines from ifconfig
def ifconfig_list (ifconfig):
    ifconfig_results = []
    ifconfig = ifconfig[ifconfig.index(eth):].splitlines()      # change 'eth' as needed for correct ifconfig results
    for i in range(3,7):
        ifconfig_results.append(ifconfig[i].strip())
    return ifconfig_results


### write ifconfig results to file
def write_results (ifconfig):           # arg is list from ifconfig_list
    for s in ifconfig:
        a.write(s + '\n')
    a.write('\n\n')


### overwrite and wipe results file
def wipe_file (backup=True):
    if backup == True:                  # creates a backup txt file and pastes the whole current results file into
        x = os.popen('date "+%D"').read().replace('/', '_').strip()     # use date in backup filename
        i_am_stupid_and_will_delete_everything_accidentally = f"results_{x}.txt"
        app = open(i_am_stupid_and_will_delete_everything_accidentally, 'a')
        app.write(r.read())
        app.close()
    w = open(ifconfigtxt, 'w')
    w.close()

#################################                               --- other helper functions
### kill running server if it doesnt automatically kill
def kill_server ():
    grep = ssh_server.ssh("ps aux | grep iperf")
    if 'iperf3' in grep:
        ssh_server.ssh("pkill iperf3")

### reset power
def onoff (outlet1=outlet1, outlet2=outlet2):
    ssh_powerswitch.ssh(f'uom set "relay/outlets/{outlet1}/state" "false"')     # outlet 1 off 
    ssh_powerswitch.ssh(f'uom set "relay/outlets/{outlet1}/state" "true"')      # outlet 1 on
    ssh_powerswitch.ssh(f'uom set "relay/outlets/{outlet2}/state" "false"')     # outlet 2 off 
    ssh_powerswitch.ssh(f'uom set "relay/outlets/{outlet2}/state" "true"')      # outlet 2 on

#################################

if __name__ == "__main__":
    wipe_file()
    a.write(header)

    for i in range(num_tests):
        print(f"power cycle...\n")
        onoff()
        sleep(30)           # takes about 25ish seconds to boot (but ssh times out at 20)
        
        print(f"\nrunning test {i+1} of {num_tests}")
        print(f"starting server on {server_ip}...\n")
        ssh_server.ssh(f"iperf3 -B {server_ip} -s")

        sleep(5)            # give the server time to get ready

        print(f"connecting to server from {client_ip}")
        print(f"running test for {seconds} seconds...\n")
        ssh_client.ssh(f"iperf3 -u -B {client_ip} -c {server_ip} -b {mbps}m -t {seconds} -l 1412 -Z")
        sleep(seconds)      # wait for test to finish
        print(f"\ntest {i+1} complete.\n") 

        client_ifconfig = ssh_client.ssh('ifconfig', readout=False)
        ifconfig = ifconfig_list(client_ifconfig)
        write_results(ifconfig)
    a.close()
