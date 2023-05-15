# generate report from test data file
from parse_functions import *

filename = "report_5_10_2023.txt"           # testfile
#filename = "test_input.txt"
file = open(filename, 'r').readlines()
filename = "report.txt"
output = open(filename, 'w')    

######################################### --- globals
N_CH = 12           # number of channels
N_LINES = len(file)
idx = 0

date = ""

tests = []
pcmout_bert = { }
linetest_in = { }

separate = "-------------------------------------------------\n"
t, n = '\t', '\n'
#########################################
""" notes and things:
bert_test_8 linetest_in results are for even numbered channels
bert_test_8r linetest_in results are for odd numbered channels


"""

def nextline(i=1):
    global idx
    idx += i

def eof():
    if idx < N_LINES:
        return False
    else:
        return True



### get test header and parameters
def get_params():
    while file[idx][0] == '-': nextline()
    line = file[idx].split()
    test_name = line[0].replace(',', '')        # test name

    i = 0
    while line[i] != "auto": i += 1
    auto_polarity = line[i+2].replace(',', '')  # auto polarity

    i = 0
    while line[i] != "data": i += 1
    data_polarity = line[i+2]                   # data polarity

    nextline()
    if file[idx][:4] == "rate":
        data_rate = file[idx].split()[2].strip()        # data rate
        if data_rate.isnumeric():
            data_rate = str(int(int(data_rate)/1000000)) + 'M'
    nextline()

    return [test_name, auto_polarity, data_polarity, data_rate]
    




### create new pcmout_bert dictionary
def make_pcmout_bert():
    global pcmout_bert
    for i in range(N_CH):
        pcmout_bert[f"ch{i}"] = []


### get channel bits and errs from pcmout bert
### { "ch0":[ [bits, errs], [bits, errs], ... ], "ch1":... }
def get_pcmout_bert(channels="all"):
    global pcmout_bert
    # create if dict is empty
    if len(pcmout_bert) == 0:
        make_pcmout_bert()


    # get values for channels
    while file[idx][0] == '-': nextline()
    keys = list(pcmout_bert)
    nextline(-1)

    # get names of fields (bits, errs, etc.)
    data = { }
    current_key = ""
    while idx < N_LINES and not("polarity = " in file[idx] or file[idx].replace('-', '') == '\n'):
        if "LINETEST IN" in file[idx]: break
        # while not end of file or next test
        if not("PCMOUT BERT" in file[idx]):
            if file[idx][0] == '-':             # (bits, errs, etc.)
                current_key = file[idx].replace('-', '').strip()
                data[current_key] = []
            else:
                data[current_key].append(file[idx].strip())
        nextline()

    
    # determine which channels have test values
    if channels == "even":
        n_ch = int(N_CH/2)
        i, x = 0, 2
    elif channels == "odd":
        n_ch = int(N_CH/2)
        i, x = 1, 2
    else:
        n_ch = N_CH
        i, x = 0, 1

    # add to dict
    data_keys = list(data)
    d_idx = len(pcmout_bert[keys[0]])
    for j in range(len(pcmout_bert)):           # new data list
        pcmout_bert[keys[j]].append([])

    for j in range(len(data)):      # for each data field
        # for 12 channels
        if len(data[data_keys[j]]) == N_CH:
            for k in range(N_CH):
                pcmout_bert[keys[k]][d_idx].append(data[data_keys[j]][k])
        # for < 12 channels
        else:
            for k in range(n_ch):
                pcmout_bert[keys[i]][d_idx].append(data[data_keys[j]][k])
        i += x






### create new linetest_in dictionary
def make_linetest_in():
    global linetest_in
    for i in range(N_CH):
        linetest_in[f"ch{i}"] = []


### get values for linetest in
### { "ch0":[ bits, errs, sync, inv, pcmin, pol_changes ], ... }
def get_linetest(channels="all"):
    global linetest_in
    # create if dict is empty
    if len(linetest_in) == 0:
        make_linetest_in()


    # get values for channels
    while file[idx][0] == '-': nextline()
    keys = list(linetest_in)
    nextline(-1)

    # if theres no LINETEST for this test
    if not("LINETEST IN" in file[idx-1]):
        return

    # get data
    data = { }
    current_key = ""
    while idx < N_LINES and not("polarity = " in file[idx] or file[idx].replace('-', '') == '\n'):
        # while not end of file or next test
        if not("LINETEST" in file[idx]):
            if file[idx][0] == '-':             # data type (bits, errs, etc.)
                current_key = file[idx].replace('-', '').strip()
                data[current_key] = []
            else:
                data[current_key].append(file[idx].strip())
        nextline()
    
    # determine which channels have test values
    if channels == "even":
        n_ch = int(N_CH/2)
        i, x = 0, 2
    elif channels == "odd":
        n_ch = int(N_CH/2)
        i, x = 1, 2
    else:
        n_ch = N_CH
        i, x = 0, 1

    # add to dict
    data_keys = list(data)
    for j in range(n_ch):
        ch_data = []
        for k in range(len(data)):       # get data for each channel
            ch_data.append(data[data_keys[k]][j])
        linetest_in[keys[i]].append(ch_data)
        i += x

    



### write parameters of individual test
def write_params(params):
    keys = list(params)
    output.write(params[keys[0]] + n)       # test name
    output.write(keys[1] + ' ' + params[keys[1]] + ', ')    # auto and data polarity
    output.write(keys[2] + ' ' + params[keys[2]] + n)
    output.write("rate = " + params[keys[3]] + n + n)





### write to file
def write_output(test):
    """
    Wed Aug 10 01:58:25 UTC 2022
    -------------------------------------------------
    bert_test_8
    auto polarity on, data polarity 0
    data rate = 50M
    -------------------------------------------------
    ch0
        pcmout_bert:  bits / errs
        linetest_in:  bits / errs, sync pass/fail, clock polarity pass/fail
    ch1
        ...
    """
    for i in range(N_CH):
        output.write(f"ch{i}\n")

        pcmout = test.ch_info(i)["pcmout_bert"]
        output.write(t + "pcmout_bert: ")
        output.write(pcmout[0] + " bits / " + pcmout[1] + " errs\n")

        linetest = test.ch_info(i)["linetest_in"]
        output.write(t + "linetest_in: ")
        output.write(linetest[0] + " bits / " + linetest[1] + " errs, ")
        output.write("sync " + linetest[2] + ", ")
        output.write("polarity changes = " + str(linetest[3]) + n)















if __name__ == "__main__":
    # get date
    while file[idx][0] == '-': nextline()
    date = file[idx].strip()
    output.write(date + n + separate)       # write date to file
    nextline()


    while idx < N_LINES:
        # get parameters
        d = build_test_dict(get_params())           # test parameters

        # if theres extra stuff after first test params
        nextline(2)
        if file[idx].split()[0].replace(',', '') != d["test name"]:
            s = ""
            while file[idx][0] != '-':
                s += file[idx]
                nextline()
            d["other stuff"] = s

        print(d["test name"]+ " " + str(idx))
    
        # for all tests in a test name
        tests = []
        while idx < N_LINES:
            # get parameters
            params = build_test_dict(get_params())          # test parameters 1

            # get polarity
            polarity = ''
            while file[idx][0] == '-':
                line = file[idx].split()
                if line[0][-8:] == "polarity":
                    polarity = line[2][0]
                    break
                nextline()
            nextline()

            # get data
            while idx < N_LINES and file[idx].replace('-', '') != n:
                if params["test name"][:10] == "bert_test_" and params["test name"][-1] == 'r':
                    get_pcmout_bert("odd")      # pcmout bert
                    get_linetest("odd")         # linetest in
                elif params["test name"][:10] == "bert_test_":
                    get_pcmout_bert("even")      # pcmout bert
                    get_linetest("even")         # linetest in
                else:
                    get_pcmout_bert("all")      # pcmout bert
                    get_linetest("all")         # linetest in

            # create test class
            tst = Test(params, pcmout_bert, linetest_in)
            tests.append(tst)             # add test info for this rate to list for this name

            if not(eof()):
                testname = file[idx+1].split()[0].replace(',', '')
                if testname != params["test name"]:
                    pcmout_bert, linetest_in = { }, { }
                    break
        
        # write to output report file
        write_params(tests[0].parameters)
        write_output(tests[0])


    output.close()
    
