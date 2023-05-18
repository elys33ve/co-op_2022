N_CH = 12           # number of channels


### dictionary for parameters
def build_test_dict(name, auto=0, data=0, rate=0):
    # if given list
    if type(name) == list:
        rate, data, auto = name[3], name[2], name[1], 
        name = name[0]

    # create dictionary
    new_dict = {}
    new_dict["test name"] = name
    new_dict["auto polarity"] = auto
    new_dict["data polarity"] = data
    new_dict["data rate"] = rate
    return new_dict



### just prints values of any dictionary w keys
def print_dict(dictionary):
    keys = list(dictionary)
    for i in range(len(keys)):
        print(f"{keys[i]}: {dictionary[keys[i]]}")





class Test (object):
    def __init__ (self, parameters, pcmout={}, linetest={}):
        self.parameters = parameters
        # { "test name":<>, "auto polarity":<>, "data polarity":<>, "data rate":<> }
        self.pcmout_bert = pcmout
        # { "ch0":[ [bits, errs], [bits, errs], ... ], "ch1":... }
        self.linetest_in = linetest
        # { "ch0":[ bits, errs, sync, inv, pcmin, pol_changes ], ... }


    def ch_dict(self, ch):
        if ch >= len(self.pcmout_bert): return { }
        ch = f"ch{ch}"

        return { "pcmout_bert":[self.pcmout_bert[ch]], "linetest_in":[self.linetest_in[ch]] }


    def ch_info(self, ch):
        if ch >= len(self.pcmout_bert): return { }
        ch = f"ch{ch}"

        # pcmout_bert: total bits / total errs
        total_bits, total_errs = 0, 0
        for i in range(len(self.pcmout_bert[ch])):
            total_bits += int(self.pcmout_bert[ch][i]["bits"])
            total_errs += int(self.pcmout_bert[ch][i]["errs"])
        pcmout = [str(total_bits), str(total_errs)]

        # linetest
        if len(self.linetest_in) == 0: return { "pcmout_bert":pcmout }  # if no linetest
        total_bits, total_errs = 0, 0
        sync_fail, polarity_changes = 0, []
        for i in range(len(self.linetest_in[ch])):
            # bits and errs
            total_bits += int(self.linetest_in[ch][i]["bits"])
            total_errs += int(self.linetest_in[ch][i]["errs"])
            # sync
            if self.linetest_in[ch][i][2] != "sync":
                sync_fail += 1
            # polarity changes
            polarity_changes.append(self.linetest_in[ch][i][4])
        if sync_fail > 0: 
            sync_fail = "fail"
        else:
            sync_fail = "pass"
        linetest = [str(total_bits), str(total_errs), sync_fail, polarity_changes]

        return { "pcmout_bert":pcmout, "linetest_in":linetest}

        


class Parameters (object):
    def __init__ (self, test_name="", auto_pol="", data_pol="", rate="", other=""):
        self.test_name = test_name
        self.auto_polarity = auto_pol
        self.data_polarity = data_pol   
        self.rate = rate
        self.other = other





class Channel (object):
    def __init__ (self, n, r):
        self.channel_number = n
        self.rate = r
        
        self.bits = []
        self.errs = []
        self.pcmin = []
        self.changes = []

        self.l_bits = []
        self.l_errs = []
        self.sync = []
        self.inv = []
        self.l_pcmin = []
        self.l_changes = []

    def empty(self, x):
        if len(x) == 0: return True
        else: return False

    def print_pcmout(self):
        print("bits: " + str(self.bits))
        print("errs: " + str(self.errs))
        print("pcmin: " + str(self.pcmin))
        print("changes: " + str(self.changes))

    def print_linetest(self):
        print("bits: " + str(self.l_bits))
        print("errs: " + str(self.l_errs))
        print("sync: " + str(self.sync))
        print("inv: " + str(self.inv))
        print("pcmin: " + str(self.l_pcmin))
        print("changes: " + str(self.l_changes))
    
    def print_some(self):
        print(f"ch{self.channel_number}")
        print(f"\t({self.bits[0]}/{self.errs[0]})")
        # sync
        sync = "all sync"
        if len(self.sync) == 0: sync = "--"
        for i in range(len(self.sync)):
            if self.sync[i] != "sync": sync = "a fuck up"
        # bits/errs
        if len(self.l_bits) == 0 or len(self.l_errs) == 0: bits, errs = '--', '--'
        else: bits, errs = self.bits[0], self.errs[0]
        print(f"\t({bits}/{errs}, {sync})")

    def write_out(self, file):
        file.write(f"\tch{self.channel_number}\n")

        # pcmout bits / errs
        bits, errs = '--', '--'
        if not(self.empty(self.bits) or self.empty(self.errs)):
            # get sums
            bits, errs = 0, 0
            for i in range(len(self.bits)):
                bits += int(self.bits[i])
                errs += int(self.errs[i])
        file.write(f"\t\tpcmout_bert: {bits} bits / {errs} errs\n")

        # linetest bits / errs
        bits, errs = '--', '--'
        if not(self.empty(self.l_bits) or self.empty(self.l_errs)):
            # get sums
            bits, errs = 0, 0
            for i in range(len(self.l_bits)):
                bits += int(self.l_bits[i])
                errs += int(self.l_errs[i])

        # linetest sync
        sync = '--'
        if not(self.empty(self.sync)):
            sync = "all sync"
            for i in range(len(self.sync)):
                if self.sync[i] != "sync":
                    sync = "weewooweewoo not sync"
        file.write(f"\t\tlineteset_in: {bits} bits / {errs} errs, {sync}\n")

    def check_pcmins(self, polarities):
        fail = False
        # pcmin (pcmout)
        if len(self.pcmin) > 0:
            for i in range(len(self.pcmin)):
                # pass: polarity=1, falling edge
                if "falling" in self.pcmin[i] and polarities[i] != 1:
                    fail = True
                    break
                # pass: polarity=0, rising edge
                if "rising" in self.pcmin[i] and polarities[i] != 0:
                    fail = True
                    break
        
        # pcmin (linetest)
        if len(self.l_pcmin) > 0:
            for i in range(len(self.l_pcmin)):
                # pass: polarity=1, falling edge
                if "falling" in self.l_pcmin[i] and polarities[i] != 1:
                    fail = True
                    break
                # pass: polarity=0, rising edge
                if "rising" in self.l_pcmin[i] and polarities[i] != 0:
                    fail = True
                    break
        return fail




class Test (object):
    def __init__ (self, data_rate, channels):
        self.data_rate = data_rate
        self.channels = channels
        self.data_polarity = -1
        self.polarities = []
    
    def pol_test(self, polarities=[]):
        if len(polarities) <= 0: polarities = self.polarities
        if len(polarities) > 0:
            fails = []
            for i in range(len(self.channels)):
                fails.append(self.channels[i].check_pcmins(polarities))
        return fails
    
    def inv_test(self):
        return
                
    
