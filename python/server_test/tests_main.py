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
from time import sleep


#################################

#################################


if __name__ == "__main__":

    #power_cycle()      # turn on

    for i in range(num_tests):
        print(f"\nrunning test {i+1} of {num_tests}")
        print(f"server = {server_ip}\tclient = {client_ip}")
        print(f"test time = {seconds} seconds\n")

        run_server()
        run_client(seconds=60)

        print(f"\ntest {i+1} complete.\n")

    

    
    #x = ssh("ifconfig")

    
