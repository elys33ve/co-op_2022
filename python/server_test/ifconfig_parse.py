# python scripts for conducting multiple tests and getting results for number of errors each trial
#
# this script is function defs for after obtaining ifconfig txt file
#   - finds rx error results
#   - records results in separate txt file (for now at least)



import os

ifconfig = "/home/fiona/projects/fi_src/python/ifconfig.txt"
results = "/home/fiona/projects/fi_src/python/test_results.txt"

#################################

def read_file (file):                   # print file contents by line to terminal (for test)
    o = open(file, 'r')
    for line in o:
        print(line)

def clear_file (file):                  # clear defult results file
    w = open(file, 'w')
    w.close()

#################################

### get list of lines with search word/term
def get_lines (word, file=ifconfig):        
    o = open(file, 'r')
    lines = []
    idx = 0

    for line in o:
        idx += 1
        if word in line:
            lines.append(idx-1)
    
    return lines


### get num rx errors from if config txt file
def get_num_errors (file=ifconfig):
    rl = open(file, 'r').readlines()

    result_lines = get_lines("RX errors ", file)
    amt = len(result_lines)

    num_errors = []

    for i in range(amt):                                    # just get number of errors
        num_errors.append(rl[result_lines[i]].strip())
        idx = num_errors[i].index("RX errors ")
        num_errors[i] = num_errors[i][idx+10:len(num_errors[i])].strip()
        num_errors[i] = num_errors[i][0:num_errors[i].index(" ")]

    
    return num_errors


### append to txt file
def append_file (result_list, new_file=False, test_num='x', filename='test_results.txt'):
    a = open(filename, 'a')

    ### ADD LATER ALSKDJFL;SAKDJF;LSAKDJ ---- if new_file == True, and defult filename exists, create new file
    ### with defult name +1 until DNE

    if test_num == 'x':         # separate each test results
        a.write("-----\n")
    else:
        a.write(f"----- test {test_num}\n")

    for i in range(len(result_list)):           # write results to file
        a.write(f"{result_list[i]}\n")

    a.close()
