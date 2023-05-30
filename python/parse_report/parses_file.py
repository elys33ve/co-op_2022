# generate report from test data file
from parse_functions import *
from parse_classes import *
import sys

######################################### --- globals
file = []
params = []         # [ test1params, test2params, test3params, ... ]
tests = []          # [ Test1, Test2, Test3, ... ]

######################################### --- functions


def output_info():
    # get lists for test names and data rates
    names = param_names(params)
    tsts = tests_sort(tests)

    # print out info
    n_tests = len(params)
    if onetest == True: n_tests = 1
    for i in range(n_tests):
        tst = tsts[i]
        print("\n\n======= " + names[i] + " =======")
        print(f"auto polarity {params[i].auto_pol}, data polarity {params[i].data_pol}")
        for j in range(len(tst)):
            # print rates
            print("\n--- " + tst[j].params.rate)
            # print individual channel info
            for k in range(N_CH):
                tst[j].channels[k].printout()
            



def do_stuff():
    starts = param_indexes(params)
    starts.append(n_lines-1)
    rates = test_indexes(tests)
    rates.append(n_lines-1)
    r_idx = 0


    # get data
    n_tests = len(params)
    if onetest == True: n_tests = 1
    for i in range(n_tests):
        idx = starts[i]
        name = params[i].test_name

        # check for pcmout
        jdx = idx
        pc_bool = False
        while not(jdx >= n_lines or r_idx >= len(rates) or jdx >= rates[r_idx+1]):
            if "PCMOUT BERT" in file[jdx]:
                pc_bool = True
                break
            jdx += 1
        if debug and not silent: print("pcmout data in ", name, ": ", pc_bool)

        # check for linetest
        jdx = idx
        ltst_bool = False
        while not(jdx >= n_lines or r_idx >= len(rates) or jdx >= rates[r_idx+1]):
            if "LINETEST IN" in file[jdx]:
                ltst_bool = True
                break
            jdx += 1
        if debug and not silent: print("linetest data in ", name, ": ", ltst_bool)


        # get test data
        while not(eof() or r_idx >= len(rates) or idx >= rates[r_idx]):
            nextline(j=rates[r_idx]-1)
            channels = tests[r_idx].channels

            # get even/odd alternating
            odd = 0
            if name[-1] == 'r':
                odd = 1

            # actually get the values
            if pc_bool == True:
                get_pcmout_bert(channels, rates[r_idx]+1, odd)     # pcmout bert
            if ltst_bool == True:
                get_linetest_in(channels, rates[r_idx]+1, odd)     # linetest in   

            tests[r_idx].channels = channels
            
            # check if next test
            r_idx += 1  
            if i+1 >= len(starts) or rates[r_idx] >= starts[i+1]:
                break
    



def print_issues(silents=[]):
    """ problems to report (for fields that are not left intentionally empty):
            bits <= 0
            errs > 0
            pcmin: falling edge != polarity 1, rising edge != polarity 0
            sync fail
            all inv either inverted or noninverted
    """
    tsts = tests_sort(tests)

    if not silent: print("\n\n\n---------------------------------------------------------------------")
    if not silent: print("--- data polarities:")
    if not silent: test_inv(tsts)
    if not silent: print("\n--- issues:")
    l = len(tsts)
    for i in range(l):
        name = tsts[i][0].get_name()
        f_bool = True

        # go through all rates in each test
        for j in range(len(tsts[i])):
            t = tsts[i][j]
            fails = t.issues(silents)
            
            if len(fails) > 0:
                # print test name if havent already
                if f_bool:
                    if not silent: print(name)
                    f_bool = False
                # print errors for range
                if not silent: print("\trate =", t.params.rate, ":   ", fail_list(fails))

        # extra newline
        if f_bool == False: 
            if not silent: print()




if __name__ == "__main__":
    file = open_file(sys.argv)
    params, tests = param_list()
    n_lines = len(file)

    do_stuff()
    if not debug and not silent: output_info()
    if not debug and not silent: print_issues(["inv"])


