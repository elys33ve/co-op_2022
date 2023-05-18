N_CH = 12           # number of channels




# just prints values of any dictionary w keys
def print_dict(dictionary):
    keys = list(dictionary)
    for i in range(len(keys)):
        print(f"{keys[i]}: {dictionary[keys[i]]}")

        

# parameters (test name, auto & data polarity, data rate)
class Parameters (object):
    def __init__ (self, test_name="", auto_pol="", data_pol="", rate="", other=""):
        self.test_name = test_name
        self.auto_polarity = auto_pol
        self.data_polarity = data_pol   
        self.rate = rate
        self.other = other




# channel class, holds pcmout bert and linetest in data
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
            
        if len(self.inv) > 0: inv = self.inv[0]
        else: inv = "--"
        file.write(f"\t\tlineteset_in: {bits} bits / {errs} errs, {inv}\n")

    def check_pcmins(self, polarities):
        # pcmin (pcmout)
        if len(self.pcmin) > 0:
            for i in range(len(self.pcmin)):
                # pass: polarity=1, falling edge
                if "falling" in self.pcmin[i] and polarities[i] != 1:
                    return False
                # pass: polarity=0, rising edge
                if "rising" in self.pcmin[i] and polarities[i] != 0:
                    return False
        
        # pcmin (linetest)
        if len(self.l_pcmin) > 0:
            for i in range(len(self.l_pcmin)):
                # pass: polarity=1, falling edge
                if "falling" in self.l_pcmin[i] and polarities[i] != 1:
                    return False
                # pass: polarity=0, rising edge
                if "rising" in self.l_pcmin[i] and polarities[i] != 0:
                    return False
        return True

    def x(self):
        if len(self.inv) > 0:
            return self.inv[0]
        else: return '---'


# Test for each data rate 
class Test (object):
    def __init__ (self, params, channels):
        self.params = params
        self.channels = channels
        self.polarities = []

    # returns True bits > 0
    def bit_pass(self):
        for i in range(len(self.channels)):
            ch = self.channels[i]
            
            # pcmout bits
            for j in range(len(ch.bits)):
                if int(ch.bits[j]) <= 0:
                    return False
            # linetest bits
            for j in range(len(ch.l_bits)):
                if int(ch.l_bits[j]) <= 0:
                    return False
        return True
                
    # returns True if errs = 0
    def err_pass(self):
        for i in range(len(self.channels)):
            ch = self.channels[i]

            # pcmout errs
            for j in range(len(ch.errs)):
                if int(ch.errs[j]) != 0:
                    return False
            # linetest bits
            for j in range(len(ch.l_errs)):
                if int(ch.l_errs[j]) != 0:
                    return False
        return True
             
    # return list of bools for pcmin fail (True), pass (False) 
    def pol_test_list(self, polarities=[]):
        if len(polarities) <= 0: polarities = self.polarities
        if len(polarities) > 0:
            passes = []
            for i in range(len(self.channels)):
                passes.append(self.channels[i].check_pcmins(polarities))
        return passes
    
    def inv_test(self):
        print(" " + self.channels[0].inv[0])
                
    


