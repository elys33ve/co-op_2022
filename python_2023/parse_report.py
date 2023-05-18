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

tests = []      # { [ [ Channel, Channel, ... ], ... ], ... ]
Tests = []      # [ Test1_50M, Test1_45M, ... , Test2_50M, Test2_45M, ...]
test_params = []


t, n = '\t', '\n'
#########################################
""" notes and things:
bert_test_8 linetest_in results are for even numbered channels
bert_test_8r linetest_in results are for odd numbered channels
"""


def nextline(i=1, j=0):
    global idx
    if j != 0: idx = j
    else: idx += i

def eof():
    if idx < N_LINES:
        return False
    else:
        return True

def dashed(s):
    s = s.strip()
    for i in s:
        if i != '-':
            return False
    return True


# get indexs with "auto polarity" and "data polarity" for parameter lines
def start_idx():
    starts, names = [], []
    prev_name = ""
    for i in range(N_LINES-1):
        if dashed(file[i]) and ("auto polarity" in file[i+1] and "data polarity" in file[i+1]):
            testname = file[i+1].strip().split()[0].replace(',', '')
            if testname != prev_name:
                prev_name = testname
                names.append(testname)
                starts.append(i+1)
    starts.append(N_LINES-1)
    return starts  

# get list of indexs with "rate = " for test start/ends
def rate_idx():
    rates = []
    for i in range(N_LINES):
        if "rate = " in file[i] and file[i].split()[2].strip().isnumeric():
            rates.append(i)
    rates.append(N_LINES-1)
    return rates




# output test results to report file
def output_tests():
    t = test_params[0].test_name
    test_names = [t]
    for i in range(len(test_params)):
        if test_params[i].test_name != t:
            t = test_params[i].test_name
            test_names.append(t)

    for i in range(len(tests)):
        tst = tests[i]
        output.write("------- " + test_names[i] + " -------\n")
        for j in range(len(tst)):
            output.write("--- " + tst[j][0].rate + n)
            for k in range(len(tst[j])):
                tst[j][k].write_out(output)
            output.write("\n")

    output.write("\n---------------------------------------------------------------------\n")
    output.write("issues:\n\n")

    x = find_issues()
    #passes = ["bits", "errs", "clock polarity", "sync"]
    
    output.write(x[0])
    output.close()



# get parameters (test name, auto polarity, data polarity, data rate)
def get_params():
    line = file[idx]
    name = line.split()[0].strip().replace(',', '')            # name
    
    auto_pol, data_pol = "--", "--"
    if "auto polarity" in line:
        x = line.index("auto polarity")
        auto_pol = line[x+14:x+17].replace(',', '')         # auto polarity
    if "data polarity" in line:
        x = line.index("data polarity")
        data_pol = line[x+14:x+17].replace(',', '')         # data polarity

    nextline()
    rate = file[idx].split()[2].strip()                     # rate
    if rate.isnumeric() and int(rate) >= 1000000: 
        rate = str(int(int(rate) / 1000000)) + 'M'

    return Parameters(name, auto_pol, data_pol, rate)



# get list of polarities
def get_polarity():
    pol, p = [], []
    for i in range(N_LINES):
        # get polarities and add to list
        if "polarity = " in file[i]:
            p.append(file[i].replace('-','').replace('polarity = ','').strip())
            if p[-1].isnumeric(): p[-1] = int(p[-1])
        elif "rate = " in file[i] and len(p) > 0:
            pol.append(p)
            p = []

    return pol



# add data to member of channels obj
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

# add values to every other channel
def ch_r(channels, key, val_list, odd=0, ltst=0):
    for i in range(len(val_list)):
        add_to(channels[odd], key, val_list[i], ltst)
        odd += 2

# create and return list of channel class instances
def create_channels(rate):
    channels = []
    for i in range(N_CH):
        channels.append(Channel(i, rate))
    return channels



# pcmout bert
def get_pcmout_bert(channels, i, odd=0):
    nextline(j=i)

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
                    add_to(channels[ch], keys[d], data[keys[d]][ch], ltst=0)
            else:                       # lest than 12 (alternate channels)
                ch_r(channels, keys[d], data[keys[d]], odd=odd, ltst=0)



# linetest in
def get_linetest_in(channels, i, odd=0):
    nextline(j=i)

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
            while file[idx][0] != '-':
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


   
# find issues
def find_issues():
    return_string = ""
    lt = len(Tests)
    tname, issues = "", [[], [], [], []]
    bits, errs, clk, sync = 0, 0, 0, 0
    errors = ""
    issues_str = ["bits <= 0: ", "errs > 0: ", "clock polarity issue: ", "sync fail: "] 
    for i in range(lt):
        # test end
        name = Tests[i].params.test_name
        if tname != name:
            tname = name

            for j in range(len(issues)):
                if issues[j] != []:
                    return_string += name +'\n\t' 
                    return_string += issues_str[j] + str(issues[j]) + '\n'
                    errors += issues_str[j]

            issues = [[],[],[],[]]

        # check
        x = Tests[i].check_all()
        for j in range(len(x)):
            if x[j] != 0:
                issues[j].append(Tests[i].params.rate)

    if "bits" in errors:
        bits = 1
    if "errs" in errors:
        errs = 1
    if "clock" in errors:
        clk = 1
    if "sync" in errors:
        sync = 1

    return return_string, [bits, errs, clk, sync]
          



if __name__ == "__main__":
    # get date
    while file[idx][0] == '-': nextline()
    date = file[idx].strip()
    nextline()


    # get start of each new test
    starts = start_idx()
    rates = rate_idx()
    r_idx = 0


    # default lists
    for i in range(len(starts)-1):
        tests.append([])
    test_params = []


    # get data
    for i in range(len(starts)-1):
        idx = starts[i]

        # get Parameters
        params = get_params()
        name = params.test_name

        # check for pcmout
        jdx = idx
        pc_bool = False
        while not(jdx >= N_LINES or r_idx >= len(rates) or jdx >= rates[r_idx+1]):
            if "PCMOUT BERT" in file[jdx]:
                pc_bool = True
                break
            jdx += 1

        # check for linetest
        jdx = idx
        ltst_bool = False
        while not(jdx >= N_LINES or r_idx >= len(rates) or jdx >= rates[r_idx+1]):
            if "LINETEST IN" in file[jdx]:
                ltst_bool = True
                break
            jdx += 1


        # get test data
        while not(eof() or r_idx >= len(rates) or idx >= rates[r_idx]):
            # get parameters
            nextline(j=rates[r_idx]-1)
            p = get_params()
            test_params.append(p)
            rate = p.rate
                

            # create new list of channel class isntances
            channels = create_channels(rate)

            # get even/odd alternating
            odd = 0
            if name[-1] == 'r':
                odd = 1

            # actually get the values
            if pc_bool == True:
                get_pcmout_bert(channels, starts[i]+5, odd)     # pcmout bert
            if ltst_bool == True:
                get_linetest_in(channels, starts[i]+4, odd)     # linetest in   
              

            # add to tests
            tests[i].append(channels)

            
            # check if next test
            r_idx += 1  
            if i+1 >= len(starts) or rates[r_idx] >= starts[i+1]:
                break


    # get test fail/pass
    polarities = get_polarity()
    Tests, p = [], 0
    lt = len(tests)

    for i in range(lt):
        t = tests[i]
        for j in range(len(t)):
            Tests.append(Test(test_params[p], t[j]))
            # add polarities
            if len(polarities) < p:
                Tests[p].polarities = polarities[p] 
            else:
                Tests[p].polarities = polarities[len(polarities)-1]
            p += 1


    # print stuff
    output_tests()



    """
    # print test_name: [rates]
    rates, tname = [], Tests[0].params.test_name
    for i in range(len(Tests)):
        name = Tests[i].params.test_name
        if tname != name:
            print(f"{name}: {rates}")
            tname, rates = name, []
        
        rate = Tests[i].params.rate
        rates.append(rate)
    """

    
        
