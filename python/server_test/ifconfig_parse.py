# python scripts for conducting multiple tests and getting results for number of errors each trial
#
# this script is function defs for after obtaining ifconfig txt file
#   - finds rx error results
#   - records results in separate txt file (for now at least)


import os

ifconfig = "/home/fiona/projects/fi_src/python/ifconfig.txt"
results = "/home/fiona/projects/fi_src/python/test_results.txt"

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
        ifconfig_results.update({f"trial {num}":errs})
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
