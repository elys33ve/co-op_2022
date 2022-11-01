# variables for the server test scripts
# - ip addresses
# - ssh class
# - commands and notes

# command line commands
"""
    ssh powerstrip:
ssh admin@powerstrip -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa
uom set "relay/outlets/1/state" "false"
uom set "relay/outlets/1/state" "true"

    iperf3 server and client:
iperf3 -B IPADDRESS -s
iperf3 -u -B IPCLIENT -c IPSERVER -b 400m -t 600 -l 1412 -Z
"""

import paramiko

############################################ --- files
ifconfig_results = {}
ifconfigtxt = "iperf3py_results.txt"

a = open(ifconfigtxt, 'a')      # append
r = open(ifconfigtxt, 'r')      # read
############################################ --- ip addresses
power_ip = '10.10.10.2'     # powerstrip -> pc
board_ip1 = '10.10.10.3'    # board -> pc
board_ip2 = '10.10.10.4'    # board -> pc
server_ip = '11.11.11.3'    # board -> board
client_ip = '11.11.11.4'    # board -> board

eth = 'eth1'        # ethernet port for ifconfig results
############################################ --- ssh
num_tests = 700     # number of tests
seconds = 10        # number of seconds tests take
mbps = 400          # mb per sec
outlet1 = 0         # number of powerstrip outlet 1
outlet2 = 1         # number of powerstrip outlet 2

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
