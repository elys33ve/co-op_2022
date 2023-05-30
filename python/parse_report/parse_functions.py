# function defs for traversing file, getting data, and such
from parse_classes import *
import sys

######################################### --- globals
N_CH = 12           # number of channels
n_lines = 0         # number of lines in file

filename = "/home/fiona/projects/fi_src/python/parse_file/report_5_10_2023.txt"       # default input file for if no args provided
file = []
idx = 0

date = ""
tests = []
params = []

######################################### --- debug functions
debug = False
silent = False
onetest = False


def pl():                       # debug function; print current line w idx
    print(idx, ":  ", file[idx])


def show_testnames(params):     # print all test names
    for p in params:
        if p.pattern != "":
            print(f"{p.test_name} ({p.pattern})")
        else:
            print(p.test_name)


def show_datafields(ch=0):      # show all non empty data fields for each channel
    x = tests_sort(tests)
    
    for i in range(len(x)):
        for j in range(len(x[i])):
            print(x[i][j].params.test_name, x[i][j].params.rate)
            x[i][j].channels[ch].datafields()
        print("\n\n")


######################################### --- short helper functions

def nextline(i=1, j=0):     # update idx
    global idx
    if j != 0: 
        idx = j
    else: 
        idx += i


def eof():                  # test if end of file (use idx)
    if idx < n_lines:
        return False
    else:
        return True


def dashed(s):              # test if line is just '-'s
    s = s.strip()
    for i in s:
        if i != '-':
            return False
    return True


def find(x):                # step through file until line with x(char) first
    while file[idx][0] == str(x): 
        nextline()


######################################### --- other helper functions


### test for args, open file, return file lines list
def open_file(sysargs):
    global file, filename, n_lines

    l_args, n_args = sysargs, len(sysargs)        # args and number of args
    
    # if 1 arg provided (input file)
    if n_args > 1:
        filename = l_args[1]

    # open file
    file = open(filename, 'r').readlines()
    n_lines = len(file)
    return file



### get parameters (test name, auto polarity, data polarity, data rate)
def get_params(k=idx):
    nextline(j=k)
    line = file[idx].strip().replace(',','').split()

    # get name
    name = line[0]

    # get auto polarity
    if "auto" in line and "polarity" in line:
        auto_pol = line[line.index("auto")+2]

    # get data polarity
    if "data" in line and "polarity" in line:
        data_pol = line[line.index("data")+2]

    # get pattern
    pattern = ''
    if line[-1] != '1' and line[-1] != '0':
        pattern = line[-1]

    # get rate
    nextline()
    rate = file[idx].split()[2].strip()                     # rate
    if rate.isnumeric() and int(rate) >= 1000000:
        rate = str(int(int(rate) / 1000000)) + 'M'
    
    return Parameters(name, auto_pol, data_pol, pattern, rate, idx-1)



### create and return list of channel class instances
def create_channels(rate):
    channels = []
    for i in range(N_CH):
        channels.append(Channel(i, rate))
    return channels



### get list of parameter class instances for tests
def param_list():
    """ look for lines:  
            "-------------------------------------------------------------"
            "<test name>, various rates, auto polarity <on/off>, data polarity <1/0>"
            "rate = 50M"
    """
    global params, tests, date
    polarities, prev = [], 0

    # get date
    if file[1][0].isupper():
        date = file[1].strip()
    # get parameters, ranges, polarities, etc. and sort into lists
    for i in range(n_lines-1):
        # get parameter lines
        if dashed(file[i]) and ("auto polarity" in file[i+1] and "data polarity" in file[i+1]):
            param = get_params(i+1)

            # test for start of next test (until different param line)
            if compare_params(params, param):
                # create Test instance for one test of 12 channels
                ch_list = create_channels(param.rate)
                tests.append(Test(param, ch_list))

                # add list of polarities to test parameters
                if len(tests) > 1:
                    tests[prev].polarities = polarities
                    polarities = []
                    prev += 1
            else:
                params.append(param)

        # get polarity lines
        elif "polarity = " in file[i]:
            if '0' in file[i]: pol = 0
            elif '1' in file[i]: pol = 1
            else: pol = '?'
            polarities.append(pol)

    tests[prev].polarities = polarities
    return params, tests



### test data polarity / inv
def test_inv(tst):
    # make sure for each test: all inverted or all noninverted, show data polarity

    for t in tst:
        name = t[0].get_name()
        data_pol = t[0].params.data_pol
        
        invs = [0, 0, 0]                # [inverted, noninverted, else]
        for i in range(len(t)):
            if t[i].get_inv() == "inverted":          # inverted ++
                invs[0] += 1
            elif t[i].get_inv() == "noninverted":     # noninverted ++
                invs[1] += 1
            elif t[i].get_inv() != -1:                  # skip if field empty, otherwise, errors ++
                invs[2] += 1

        # test if same
        if invs[0] > 0 and invs[1] == 0 and invs[2] == 0:       # inverted
            inv = "inverted"
        elif invs[0] == 0 and invs[1] > 0 and invs[2] == 0:     # noninverted
            inv =  "noninverted"
        elif invs[0] == 0 and invs[1] == 0 and invs[2] == 0:    # empty
            inv =  -1
        else:                                                   # errors
            inv =  "inv data issue (inverted/noninverted varies)"

        # printout
        if inv != -1: 
            print(f"{name}:   data polarity {data_pol},   {inv}\n")
        else:
            print(f"{name}:   data polarity {data_pol},   ---\n")


######################################### --- get functions


### get test start indexes from params
def param_indexes(params):
    idxs = []
    for p in params:
        idxs.append(p.index)
    return idxs



### get individual test indexes from Test list
def test_indexes(tests):
    idxs = []
    for t in tests:
        idxs.append(t.params.index)
    return idxs



### get test rates, sort into a list of lists of same test name 
def tests_sort(tests, rate=0):
    tst, tmp = [], []
    pname = tests[0].params.test_name

    for t in tests:
        # add sublist to rates when test name different
        if t.params.test_name != pname:
            tst.append(tmp)
            tmp, pname = [], t.params.test_name

        # if not rate (default): list of Test class instances
        if rate == 0:
            tmp.append(t)
        # if rate param set: list of test rates
        elif rate != 0:
            tmp.append(t.params.rate)
    tst.append(tmp)

    return tst



### get name and add pattern if incuded (tst = Parameters class)
def get_name(tst):
    # if there is pattern
    if tst.pattern != "":
        return f"{tst.test_name} {tst.pattern}"
    else:
        return tst.test_name


### get list of test names
def param_names(params):
    names = []
    for p in params:
        names.append(get_name(p))
    return names


######################################### --- get data functions



### add data to member of channels obj
def add_to(obj, key, val, ltst=0):
    # pcmout bert
    if key == "bits" and ltst == 0:
        obj.bits.append(val)
    elif key == "errs" and ltst == 0:
        obj.errs.append(val)
    elif key == "pcmin clock polarity" and ltst == 0:
        obj.pcmin.append(val)
    elif key == "polarity changes" and ltst == 0:
        obj.changes.append(val)
    # linetest
    elif key == "bits":
        obj.l_bits.append(val)
    elif key == "errs":
        obj.l_errs.append(val)
    elif key == "sync":
        obj.sync.append(val)
    elif key == "inv":
        obj.inv.append(val)
    elif key == "pcmin clock polarity":
        obj.l_pcmin.append(val)
    elif key == "polarity changes":
        obj.l_changes.append(val)


### add values to every other channel
def ch_r(channels, key, val_list, odd=0, ltst=0):
    for i in range(len(val_list)):
        add_to(channels[odd], key, val_list[i], ltst)
        odd += 2







### pcmout bert
def get_pcmout_bert(channels, i, odd=0):
    nextline(j=i)
    if debug and not silent: print(f"pcmout run (idx: {idx})")

    # if theres a comment line kinda thing
    if file[idx] != file[idx-4]:
        while not(eof() or "polarity = " in file[idx]): nextline()


    # store data
    # sets = [ {"bits":[...], "errs":[...], ...}, ... ]
    data, sets, key = { }, [], ""
    while not (eof() or dashed(file[idx])):
        while not(eof() or dashed(file[idx]) or "PCMOUT BERT" in file[idx]): nextline()
        nextline()
        while not (eof() or dashed(file[idx]) or "LINETEST IN" in file[idx] or "polarity = " in file[idx]):
            # find keys/field names ("bits", "errs", etc.)
            key = file[idx].strip().replace('-', '')
            data[key] = []
            nextline()
            
            # get data
            while file[idx][0] != '-':
                data[key].append(file[idx].strip())
                nextline()

        # store dict in list for that test set
        sets.append(data)
        data = { }

    # if something dumb occured and data empty
    if len(sets) == 0: return       
    # delete unneccessary items in list
    t = []
    for i in range(len(sets)):
        if not(len(sets[i]) == 0 or type(sets[i]) == list or "bits" not in list(sets[i])):    
            t.append(sets[i])
    sets = t

    # store in class instance
    keys = list(sets[0])
    
    for s in range(len(sets)):
        data = sets[s]
        for d in range(len(data)):
            if len(data[keys[d]]) == N_CH:       # if 12 values
                for ch in range(N_CH):
                    add_to(channels[ch], keys[d], data[keys[d]][ch], ltst=0)
            else:                       # lest than 12 (alternate channels)
                ch_r(channels, keys[d], data[keys[d]], odd=odd, ltst=0)




### linetest in
def get_linetest_in(channels, i, odd=0):
    nextline(j=i)
    if debug and not silent: print(f"linetest run (idx: {idx})")

    # if theres a comment line kinda thing
    if file[idx] != file[idx-4]:
        while not(eof() or "polarity = " in file[idx]): nextline()


    # store data
    # sets = [ {"bits":[...], "errs":[...], ...}, ... ]
    data, sets, key = { }, [], ""
    while not (eof() or dashed(file[idx])):
        while not(eof() or dashed(file[idx]) or "LINETEST IN" in file[idx]): nextline()
        nextline()
        while not (eof() or dashed(file[idx]) or "polarity = " in file[idx]):
            # find keys/field names ("bits", "errs", etc.)
            key = file[idx].strip().replace('-', '')
            data[key] = []
            nextline()
            
            # get data
            while not eof() and file[idx][0] != '-':
                data[key].append(file[idx].strip())
                nextline()
            
        # store dict in list for that test set
        sets.append(data)
        data = { }

    if len(sets) == 0: return       # if something dumb occured and data empty
    # delete unneccessary items in list
    t = []
    for i in range(len(sets)):
        if not(len(sets[i]) == 0 or type(sets[i]) == list or list(sets[i])[0] != 'bits'):    
            t.append(sets[i])
    sets = t
    
    
    # store in class instance
    keys = list(sets[0])
    for s in range(len(sets)):
        data = sets[s]
        for d in range(len(data)):
            if len(data[keys[d]]) == N_CH:       # if 12 values
                for ch in range(N_CH):
                    add_to(channels[ch], keys[d], data[keys[d]][ch], ltst=1)
            else:                       # lest than 12 (alternate channels)
                ch_r(channels, keys[d], data[keys[d]], odd=odd, ltst=1)


