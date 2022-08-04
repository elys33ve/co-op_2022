# functions for searching and displaying info from dts file
# eventually something like "dts-parser <file> <search str>" to do stuff


# --- still need to review some parameters  and first functions cuz idr what i was doing w those ---

##### file stuff for testing
from cmath import inf


txt = "/home/fiona/Documents/test.txt"      # txt file for testing stuff
dts = "/home/fiona/dt.dts"                  # the actual file
f = open(dts, 'r')                          # --- defult file to open atm ---
        


##################################################################


### return bool for if str exists in file
def get_exist (search_str, file=dts):       # (search str, file)
    o = open(file, 'r')
    idx = 0                 # current index
    exist = False

    for line in o:          # if string exists in file, return True
        idx += 1
        if search_str in line:
            exist = True
            break
    return exist


### return list of line numbers for each search str occurence
def get_lines (search_str, file=dts):       # (search str, file)
    o = open(file, 'r')
    idx = 0                 # current index
    line_list = []          # lines str appears

    for line in o:
        idx += 1
        if search_str in line:
            line_list.append(idx-1)         # add line num to list
    return line_list




##################################################################

### print line(s) by line number
def show_lines (lines, file=dts):   # (list of lines to print, file)
    l = open(file, 'r').readlines()
    
    if type(lines) == type("string"):       #yes i know there are better ways im fizign ahtings rn
        lines = get_lines(lines, file)
        for i in range(len(lines)):
            print(l[lines[i]])
    elif type(lines) == type(1):              # single line (int)
        print(l[lines])
    else:                                   # multiple lines (list)
        for i in range(len(lines)):
            print(l[lines[i]])


### print out info
def show_info (things, s, file=dts):       # (dictionary, list of strings, file)
    l = open(file, 'r').readlines()                     # ^ ["channel", "ch", "channel_in", "channel_out", "line_test"]
    num = len(things)                                   # ^ [keyword/title, output title each?, outputs]
    keys = list(things)

    for i in range(num):
        print(f"{s[1]}{i}:")
        for j in range(len(things[keys[i]])):
            print(f"\t{s[j+2]}: {things[keys[j]][j]}")


### order and return channels
def get_channels (file=dts):
    l = open(file, 'r').readlines()
    channels = {}                       # ordered dictionary to return
    reg = []

    ch_lines = get_lines("channel@")        # get start line number for each channel info
    ch_num = get_lines("channel_number")    # channel numbers (line nums)

    num = len(ch_lines)                     # number of channels


    for i in range(num):            # get ch numbers and register lines
        ch_num[i] = int(l[ch_num[i]].replace("channel_number = <", "").replace(">;", "").strip(), 0)


        for j in range(10):                         # look 10 lines after 'channel@'
            if "reg =" in l[ch_lines[i] + j]:
                reg.append(l[ch_lines[i] + j].replace("reg = ", "").replace('<','').replace('>;', '').strip())
                break
    
    for i in range(num):            # format reg into [ch_in, ch_out, ln_test]
        reg[i] = reg[i].split(" ")
        reg_num = len(reg[i])   
        for j in range(reg_num):                    # separate addresses
            if len(reg[i][j]) >= len(max(reg[i], key=len)):
                reg[i].append(reg[i][j])
        del reg[i][0:reg_num]

    for i in range (num):           # get order and add to dict
        idx = ch_num.index(min(ch_num))
        channels[ch_num[idx]] = reg[idx]
        ch_num[idx] = max(ch_num) + 10

    outwords = ["channel", "ch", "channel_in","channel_out", "line_test"]
        ##### ----  REPLACE WITH [keyword, "ch" or keyword[0:2], and find the list of names in the dts file for the rest]

    show_info(channels, outwords, file)

"""         ^^ should work instead
    ch_num = list(channels)                 # dictionary keys list (ch numbers ordered)
    for i in range(num):
        print(f"ch{ch_num[i]}")
        print(f"\tchannel_in: {channels[ch_num[i]][0]}")
        print(f"\tchannel_out: {channels[ch_num[i]][1]}")
        print(f"\tline_test: {channels[ch_num[i]][2]}")
"""

#---------- merge these two functions (channel and get things)
# have them return dictionary, and maybe seperate print function idky

### order and return clocktrack                 ----------- it works for now but fix later, also make general function for dictionary (also this one doesnt order)
def get_things (s="clocktrack", file=dts):
    l = open(file, 'r').readlines()
    things = {}                         # ordered dictionary to return
    reg = []

    ch_lines = get_lines(f"{s}@")        # get start line number for each channel info
    num = len(ch_lines)

    for i in range(num):
        for j in range(25):
            if "reg =" in l[ch_lines[i] + j]:
                reg.append(l[ch_lines[i] + j].replace("reg = ", "").replace('<','').replace('>;', '').strip())
                break

    for i in range(num):
        reg[i] = reg[i].split(" ")
        reg_num = len(reg[i])   
        for j in range(reg_num):
            if len(reg[i][j]) >= len(max(reg[i], key=len)):
                reg[i].append(reg[i][j])
        del reg[i][0:reg_num]

    for i in range(num):
        things[i] = reg[i]

    outwords = [s, "ch?for now", "address: (for now)"]
    # change those later

    show_info(things, outwords, file)

"""
    for i in range(num):                            # probably change the outputs to make more sense too
        print(f"ch{i}")
        print(f"\t{s}_address: {things[i][0]}") 
"""
