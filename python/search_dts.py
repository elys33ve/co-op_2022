# functions for searching and displaying info from dts file
# eventually something like "dts-parser <file> <search str>" to do stuff


# --- still need to review some parameters  and first functions cuz idr what i was doing w those ---

##### file stuff for testing
txt = "/home/fiona/Documents/test.txt"      # txt file for testing stuff
dts = "/home/fiona/dt.dts"                  # the actual file
f = open(dts, 'r')                          # --- defult file to open atm ---
        


##################################################################


### return bool for if str exists in file
def get_exist (search_str, file=dts):         # (search str, file)
    o = open(file, 'r')
    idx = 0
    exist = False

    for line in o:
        idx += 1
        if search_str in line:
            exist = True
            break

    return exist


### return list of line numbers for each search str occurence
def get_lines (search_str, file=dts):         # (search str, file)
    o = open(file, 'r')
    idx = 0                 # current index
    flag = 0                # num of appearences
    line_list = []          # lines str appears

    for line in o:
        idx += 1
        if search_str in line:
            flag += 1                   # flag appearence
            line_list.append(idx-1)     # add line num to list
    
    return line_list




##################################################################

### print line(s) by line number
def show_lines (lines, file=dts):   # (list of lines to print, file)
    l = open(file, 'r').readlines()
    
    if type(lines) == type(1):              # single line (int)
        print(l[lines])
    else:                                   # multiple lines (list)
        for i in range(len(lines)):
            print(l[lines[i]])




### print channels
def show_channels (file=dts):               # (search str, file)
    l = open(file, 'r').readlines()

    line_num = get_lines("channel@")        # list of line numbers
    ch_num = len(line_num)                  # number of channels

    channels, reg = [], []                  # channels and registers
    ch_in, ch_out, ln_tst = [], [], []      # channel in, channel out, and line test


    for i in line_num:              # format channel names
        channels.append(l[i].replace('{',' ').strip())

    for i in range(ch_num):         # add register lines to list
        for j in range(10):                                 # 10 lines under channel@'s
            if "reg =" in l[line_num[i] + j]:
                reg.append(l[line_num[i] + j].replace("reg = ", "").replace('<','').replace('>;', '').strip())
                break
    
    for i in range(ch_num):         # get in, out, and line test from reg
        reg[i] = reg[i].split(" ")
        reg_num = len(reg[i])
        for j in range(reg_num):                            # separate addresses
            if len(reg[i][j]) >= len(max(reg[i], key=len)):
                reg[i].append(reg[i][j])
        del reg[i][0:reg_num]
        ch_in.append(reg[i][0])                             # add to in, out, and line test lists
        ch_out.append(reg[i][1])
        ln_tst.append(reg[i][2])

    for i in range(ch_num):         # print channel info
        print(f"ch{i}:")
        print(f"\tchannel_in: {ch_in[i]}")
        print(f"\tchannel_out: {ch_out[i]}")
        print(f"\tline_test: {ln_tst[i]}\n")



