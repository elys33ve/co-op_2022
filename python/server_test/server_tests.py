# python scripts for conducting multiple tests and getting results for number of errors each trial
# 
# this script is function defs for the command line stuff
#   - turn on power (and wait for board to boot)
#   - ssh into board
#   - run server test on board
#   - run client test on pc (and wait for test to finish)
#   - run ifconfig on board (and get temp txt file of results)
#
# ssh into board:
#   ssh alarm@tmoip-12ch
# 
# run on board/server:
#   iperf3 -B <board/server> -s
# run on pc/client:
#   iperf3 -u -B <pc/client> -c <board/server> -b 200m -t 10 -l 1412 -Z
#
# os.system("<command>"), os.popen("<command>")
# https://janakiev.com/blog/python-shell-commands/

import os
import subprocess as sp

#################################

#################################


### turn on power (and wait for board to boot)
def power_on ():
    return 0

### ssh into board
def ssh ():
    return 0

### run server test on board
def run_server ():
    return 0

### run client test on pc (and wait for test to finish)
def run_client ():
    return 0

### run ifconfig on board (and get temp txt file of results)
def get_ifconfig ():
    ifconfig = os.popen("ifconfig").read()
