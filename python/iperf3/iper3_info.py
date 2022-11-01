# variables for the server test scripts
# - ip addresses of the different things
# - commands
# - notes

# command line commands
"""
    ssh powerstrip:
ssh admin@powerstrip -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa
uom set "relay/outlets/1/state" "false"
uom set "relay/outlets/1/state" "true"

    iperf3 server and client:
iperf3 -B IPADDRESS -s
iperf3 -u -B IPCLIENT -c IPSERVER -b 400m -t 600 -l 1412 -Z

    kill server that shouldnt be running but is for some reason:
ps aux | grep iperf
kill PID

    modify wired ip address on board:
sudo nano /etc/systemd/network/eth1.network
# modify Address and save
sudo reboot

"""

from time import sleep
import paramiko, os

############################################ --- files
ifconfig_results = {}
ifconfigtxt = "ifconfig_results.txt"

a = open(ifconfigtxt, 'a')      # append
r = open(ifconfigtxt, 'r')      # read
#w = open(ifconfigtxt, 'w')      # write (overwrites)
############################################ --- ip addresses
board_ip1 = '10.10.10.3'
board_ip2 = '10.10.10.4'
server_ip = '11.11.11.3'
client_ip = '11.11.11.4'
power_ip = '10.10.10.2'

eth = 'eth1'            # ethernet port for ifconfig results
############################################ --- ssh
num_tests = 700     # number of tests to do
seconds = 10        # number of seconds tests take
mbps = 400          # mb per sec
outlet1 = 0         # number of powerstrip outlet 1
outlet2 = 1         # number of powerstrip outlet

port = 5201         # 5201 is defult for iperf3
############################################ --- functions/classes

class SSH:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password


    def print_self (self):
        print(f"host: {self.host}\t{type(self.host)}")
        print(f"username: {self.username}\t{type(self.username)}")
        print(f"password: {self.password}\t{type(self.password)}")


        ### ssh
    def ssh (self, command, readout='x'):
        host = self.host
        username = self.username
        password = self.password

        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command(command)
                      
        if readout == False:
            output = _stdout.read().decode()
            client.close()
            return output
        elif readout == True:
            output = _stdout.read().decode()
            client.close()
            print(output)
        else:
            output = f"_stderr = {_stderr}\n_stdout = {_stdout}"
            client.close()
            return output


########################################### -- unused functions i think

### get info from ifconfig string
def get_info (term, ifconfig):
    errs = []
    while term in ifconfig:
        idx = ifconfig.index(term) + len(term)+1                # idx first error result
        ifconfig = ifconfig.replace(ifconfig[0:idx], '')        # replace everything before
        idx = ifconfig.index(" ")                           # idx next space
        errs.append(ifconfig[0:idx])                        # add everything before to list (errors number)
    return errs

### gets errors number results from ifconfig output and adds to dict
def ifconfig_parse (num='x'):
    rxp = get_info("RX packets")
    rxe = get_info("RX errors")
    txp = get_info("TX packets")
    txe = get_info("TX errors")
    ifconfig_results[num] = [rxp, rxe, txp, txe]

### print and format info from ifconfig
def print_info ():
    err = ["RX packets", "RX errors", "TX packets", "TX errors"]
    keys = list(ifconfig_results)

    for i in range(len(ifconfig_results)):
        print(f"\n{keys[i]}")
        for j in range(len(ifconfig_results[keys[i]])):
            print(f"\t{err[j]}: {ifconfig_results[keys[i]][j]}")

############################################


