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

import os
import iperf3
import time

#################################

#################################


### turn on power (and wait for board to boot)
def power_on ():
    return 0

### ssh into board
def ssh ():
    return 0

### run server test on board
def run_server (seconds=10):
    server = iperf3.Server()
    server.bind_address = asdf
    server.port = 5201
    server.verbose = False

    start_time, now = time.time(), 0
    while now < start_time+seconds:
        server.run()
        now = time.time()
    
    print('stopped')


### run client test on pc (and wait for test to finish)
def run_client ():
    return 0

### run ifconfig on board (and get temp txt file of results)
def get_ifconfig ():
    ifconfig = os.popen("ifconfig").read()
    return ifconfig
