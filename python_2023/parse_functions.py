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
            total_bits += int(self.pcmout_bert[ch][i][0])
            total_errs += int(self.pcmout_bert[ch][i][1])
        pcmout = [str(total_bits), str(total_errs)]

        # linetest
        

        total_bits, total_errs = 0, 0
        sync_fail, polarity_changes = 0, []
        for i in range(len(self.linetest_in[ch])):
            # bits and errs
            total_bits += int(self.linetest_in[ch][i][0])
            total_errs += int(self.linetest_in[ch][i][1])
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

        

