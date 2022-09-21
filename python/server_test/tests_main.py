# python scripts for conducting multiple tests and getting results for number of errors each trial
# needs to:
#   - turn on power
#   - wait for board to boot
#   - ssh into board 
#   - run server test on board
#   - connect to server from pc
#   - wait for client to finish test
#   - run ifconfig on board -- (output results to temp txt file)
#   - get errors from ifconfig output
#   - record errors from each trial in separate txt file

from ifconfig_parse import *        # file and parsing stuff
from server_tests import *          # command line stuff

#################################
num_tests = 1       # number of tests to do

#################################


if __name__ == "__main__":
    """
    #power_cycle(1)     # turn on
    
    # *wait for board to boot*
    for i in range(num_tests):
        run_server()
        run_client()


    """


    x = ssh('ifconfig')
    y = ifconfig_parse(x)
    print(y)
