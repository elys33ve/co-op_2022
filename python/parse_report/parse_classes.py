# class objects defs for data
import sys

""" (for test file report_5_16_2023.txt)
7 tests
    10 tests
--------------
bert_test_8 
    pcmout: bits, errs
    (even ch#) linetest: bits, errs, sync, inv, pcmin, pol

bert_test_7
    pcmout: bits, errs, (even ch#) pcmin, pol

bert_test_8 (PN6)
    pcmout: bits, errs
    (even ch#) linetest: bits, errs, sync, inv, pcmin, pol

bert_test_7 (PN6)
    pcmout: bits, errs, (even ch#) pcmin, pol

bert_test_8r
    pcmout: bits, errs
    (odd ch#) linetest: bits, errs, sync, inv, pcmin, pol

bert_test_6
    (odd ch#) linetest: bits, errs, sync, inv, pcmin, pol

bert_test_6r
    (odd ch#) linetest: bits, errs, sync, inv, pcmin, pol

"""

######################################### 

def empty(lst):
        if len(lst) > 0:
            return False
        return True



######################################### 





### Parameters (test name, auto & data polarity, data rate)
class Parameters (object):
    def __init__ (self, test_name="", auto_pol="", data_pol="", pattern="", rate="", index=0):
        self.test_name = test_name
        self.auto_pol = auto_pol
        self.data_pol = data_pol   
        self.pattern = pattern
        self.rate = rate
        self.index = index

    def get_list(self):
        return [self.test_name, self.auto_pol, self.data_pol, 
                self.pattern, self.rate, self.index]
    
    def printout(self):
        if self.pattern != "":
            print(f"{self.test_name}, auto polarity {self.auto_pol}, data polarity {self.data_pol}, {self.pattern}")
        else:
            print(f"{self.test_name}, auto polarity {self.auto_pol}, data polarity {self.data_pol}")
        print(f"\trate = {self.rate}")






### Channel class, holds pcmout bert and linetest in data
class Channel (object):
    def __init__ (self, n, r):
        self.ch_num = n
        self.rate = r
        
        # pcmout bert
        self.bits = []
        self.errs = []
        self.pcmin = []
        self.changes = []
        # linetest in
        self.l_bits = []
        self.l_errs = []
        self.sync = []
        self.inv = []
        self.l_pcmin = []
        self.l_changes = []
    
    # get functions (test if empty, get sum, etc.)
    def get_dict(self):
        pcmout = [self.bits, self.errs, self.pcmin, self.changes]
        linetest = [self.l_bits, self.l_errs, self.sync, self.inv, self.l_pcmin, self.l_changes]
        return {"pcmout":pcmout, "linetest":linetest}

    def get_bits(self, l=0):
        # pcmout or linetest bits
        if l == 0: 
            bits = self.bits
        else: 
            bits = self.l_bits

        if empty(bits): return -1      # if no data

        # change type to int
        for i in range(len(bits)):
            bits[i] = int(bits[i])

        # return sum of bits
        return sum(bits)
    
    def get_errs(self, l=0):
        # pcmout or linetest errs
        if l == 0: 
            errs = self.errs
        else: 
            errs = self.l_errs

        if empty(errs): return -1      # if no data

        # change type to int
        for i in range(len(errs)):
            errs[i] = int(errs[i])

        # get sum of errs
        return sum(errs)
    
    def get_sync(self):
        if empty(self.sync): return -1      # if no data
        # test if all sync
        for sync in self.sync:
            if sync != "sync":
                return "fail"
        return "pass"
    
    def get_inv(self):
        if empty(self.inv): return -1      # if no data

        # get amt of inverted and noninverted
        invert, noninv = 0, 0
        for inv in self.inv:
            if inv == "inverted":
                invert += 1
            elif inv == "noninverted":
                noninv += 1

        # check if all inv, non-inv, or mix
        if invert > 0 and noninv == 0:          # only inverted
            return "inverted"
        elif invert == 0 and noninv > 0:        # only noninverted
            return "noninverted"
        elif invert == 0 and noninv == 0:       # neither?
            return "inv neither?"
        else:                                   # both?
            return "inverted & noninverted (seems problematic)"

    # print channel data
    def printout(self):
        # print channel name
        print(f"\tch{self.ch_num}")

        # get pcmout bert data
        bits = self.get_bits()
        errs = self.get_errs()

        # print pcmout bert data
        if bits != -1:
            print(f"\t\tpcmout_bert: {bits} bits/{errs} errs")
        else:
            print(f"\t\tpcmout_bert: --")

        # get linetest in data
        bits = self.get_bits(l=1)
        errs = self.get_errs(l=1)
        sync = self.get_sync()
        inv = self.get_inv()

        # print linetest in data
        if bits != -1:
            print(f"\t\tlinetest_in: {bits} bits/{errs} errs, sync {sync}, {inv}")
        else:
            print(f"\t\tlinetest_in: --")

    # test which data fields are not empty
    def datafields(self):       # show all non empty data fields for channel
        d = self.get_dict()

        # pcmout fields
        pcmout = ["bits", "errs", "pcmin clock polarity", "polarity changes"]
        s = ""
        for i in range(4):
            x = d["pcmout"][i]
            if len(x) > 0:
                s += pcmout[i] + ", "
        print(f"\tpcmout_bert: {s}")

        # linetest fields
        linetest = ["bits", "errs", "sync", "inv", "pcmin clock polarity", "polarity changes"]
        s = ""
        for i in range(6):
            x = d["linetest"][i]
            if len(x) > 0:
                s += linetest[i] + ", "
        print(f"\tlinetest_in: {s}")

    # find issues/errors
    def bit_fail(self, l=0):
        # pcmout or linetest
        if l == 0: 
            bits = self.bits
        else: 
            bits = self.l_bits

        if empty(bits): return -1      # if no data

        # test if bits > 0
        for b in bits:
            if int(b) < 1:
                return True
        return False

    def err_fail(self, l=0):
        errs = self.get_errs(l)

        if errs == 0: 
            return False
        elif errs > 0:
            return True
        else:
            return errs

    def pcmin_fail(self, polarities, l=0):
        # pcmout or linetest pcmin clock polarity
        if l == 0: 
            pcmin = self.pcmin
        else: 
            pcmin = self.l_pcmin

        if empty(pcmin): return -1      # if no data

        # test len of polarity list bc i feel like this could be an issue
        if len(polarities) != len(pcmin):
            print("(file: parse_classes.py, Channel.pcmin_fail())")
            print("smthn messed up with polarities list or linetest/pcmout get function probably")
        rng = min(len(polarities), len(pcmin))  

        # passes if all falling = polarity 1 and rising = polarity 0
        for i in range(rng):
            if polarities[i] == 1 and "falling" not in pcmin[i]:
                return True
            elif polarities[i] == 0 and "rising" not in pcmin[i]:
                return True
        return False
    
    def sync_fail(self):
        if self.get_sync() == "fail":
            return True
        elif self.get_sync() == "pass":
            return False
        else:
            return -1
       
    def inv_fail(self, params):
        inv = self.get_inv()
        name = params.test_name
        data_pol = params.data_pol

        # if no data
        if inv == -1:
            return inv

        # for all but bert_test_6:
        if "bert_test_6" not in name:
            if data_pol == 0 and inv == "noninverted":
                return False
            if data_pol == 1 and inv == "inverted":
                return False
        # bert_test_6
        else:
            if data_pol == 1 and inv == "noninverted":
                return False
            if data_pol == 0 and inv == "inverted":
                return False
        return True






### Test for each data rate 
class Test (object):
    def __init__ (self, params, channels=[]):
        self.params = params
        self.channels = channels
        self.polarities = []

    def get_name(self):
        # if there is pattern
        if self.params.pattern != "":
            return f"{self.params.test_name} {self.params.pattern}"
        else:
            return self.params.test_name

    def issues(self, silents=[]):
        fails_list = []

        # look for problems in each channel
        for ch in self.channels:
            fails = {"pcmout_bert":[], "linetest_in":[]}
            errors = False

        # pcmout_bert
            # bits
            if "bits" not in silents:
                if ch.bit_fail() != False and not ch.bit_fail() == -1:
                    fails["pcmout_bert"].append(f"bits")
                    errors = True
            
            # errs
            if "errs" not in silents:
                if ch.err_fail() != False and not ch.err_fail() == -1:
                    fails["pcmout_bert"].append(f"errs")
                    errors = True

            # pcmin
            if "pcmin" not in silents:
                if ch.pcmin_fail(self.polarities) != False and not ch.pcmin_fail(self.polarities) == -1:
                    fails["pcmout_bert"].append(f"clock polarity")
                    errors = True

        # linetest_in
            # bits
            if "bits" not in silents:
                if ch.bit_fail(1) != False and not ch.bit_fail(1) == -1:
                    fails["linetest_in"].append(f"bits")
                    errors = True
            
            # errs
            if "errs" not in silents:
                if ch.err_fail(1) != False and not ch.err_fail(1) == -1:
                    fails["linetest_in"].append(f"errs")
                    errors = True

            # sync
            if "sync" not in silents:
                if ch.sync_fail() != False and not ch.sync_fail() == -1:
                    fails["linetest_in"].append(f"sync")
                    errors = True

            # inv
            if "inv" not in silents:
                if ch.inv_fail(self.params) != False and not ch.inv_fail(self.params) == -1:
                    fails["linetest_in"].append(f"inv")
                    errors = True


            # pcmin
            if "pcmin" not in silents:
                if ch.pcmin_fail(self.polarities, 1) != False and not ch.pcmin_fail(self.polarities, 1) == -1:
                    fails["linetest_in"].append(f"pcmin")
                    errors = True


            # add channel number if any errors/issues
            if errors: 
                fails["ch"] = ch.ch_num
                fails_list.append(fails)

        return fails_list
    
    def get_inv(self):
        # get inv for all channels
        invs = [0, 0, 0]                # [inverted, noninverted, else]
        for ch in self.channels:
            if ch.get_inv() == "inverted":          # inverted ++
                invs[0] += 1
            elif ch.get_inv() == "noninverted":     # noninverted ++
                invs[1] += 1
            elif ch.get_inv() != -1:                  # skip if field empty, otherwise, errors ++
                invs[2] += 1

        #print(f"{self.params.rate} {invs}")
        
        # test if same
        if invs[0] > 0 and invs[1] == 0 and invs[2] == 0:       # inverted
            return "inverted"
        elif invs[0] == 0 and invs[1] > 0 and invs[2] == 0:     # noninverted
            return "noninverted"
        elif invs[0] == 0 and invs[1] == 0 and invs[2] == 0:    # empty
            return -1
        else:                                                   # errors
            return "inv data issue (inverted/noninverted varies)"





######################################### --- functions

### test if two parameter class instances contain the same member values (exluding rate)
### (if p1 is list then itll test if p2 is in p1)
def compare_params(p1, p2):
    # l1 == l2: True, l1 != l2: False
    # for two class objects
    if type(p1) == Parameters:
        l1, l2 = p1.get_list(), p2.get_list()

        for i in range(len(l1)-2):
            if l1[i] != l2[i]:
                return False
        return True
    # l2 in l1(list): True, l2 not in l1(list): False 
    # for list and class obj
    elif type(p1) == list:

        # iterate thru objs in list
        for i in range(len(p1)):
            # call recursively for each list item
            x = compare_params(p1[i], p2)
            if x == True: return True
    return False


### simplified list thing for Test.issues() bc i made shits unnecessarily complicated
def fail_list(fails):
    # {"ch":[...], "pcmout_bert":[[...],[...],...], "linetest_in":[[...],[...],...]}
    fstr = []
    for i in range(len(fails)):
        ch = fails[i]["ch"]
        s = []

        # pcmout_bert
        pcmout = fails[i]["pcmout_bert"]
        for j in pcmout:
            if j not in s:
                s.append(j)

        # linetest_in
        linetest = fails[i]["linetest_in"]
        for j in linetest:
            if j not in s:
                s.append(j)

        s = ", ".join(s)
        fstr.append(f"ch{ch} ({s})")

    # add to str for rate
    return ", ".join(fstr)


######################################### --- printout test functions

### print for Parameters class list
def print_params(params):
    for p in params:
        print(f"{p.test_name}, auto polarity {p.auto_pol}, data polarity {p.data_pol}, {p.pattern}, rate={p.rate} ({p.index})")


### print for Test class list
def print_tests(tests):
    pname = ""
    for t in tests:
        if t.params.test_name != pname:
            pname = t.params.test_name
            print()
        print(f"{t.params.test_name}, rate={t.params.rate}, {len(t.channels)} channels")
        print(t.polarities)












