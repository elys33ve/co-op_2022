# functions for searching and displaying info from dts file
# eventually something like "dts-parser <file> <search str>" to do stuff


##### file stuff for testing
txt = "/home/fiona/Documents/test.txt"      # txt file for testing stuff rn
dts = "/home/fiona/dt.dts"                  # the actual file


#############################################################################################

### return list of line numbers for each search str word occurence
def get_lines (word, file=dts):       # (search str, file) 
    o = open(file, 'r')
    idx = 0                 # current index
    line_list = []          # line numbers str appears

    for line in o:
        idx += 1
        if word in line:
            line_list.append(idx-1)         # add line num to list
    return line_list


### print line(s) by line number
def show_lines (lines, file=dts):       # (list of lines to print, file)
    l = open(file, 'r').readlines()
    
    if type(lines) == str:                  # if arg is string --> search for word, then print
        lines = get_lines(lines, file)
        for i in range(len(lines)):
            print(l[lines[i]])
    elif type(lines) == type(1):            # if single line (int)
        print(l[lines])
    else:                                   # if multiple lines (list)
        for i in range(len(lines)):
            print(l[lines[i]])


### print dictionary info
def show_info(things, file=dts):        # (dictionary from get_things, file)
    l = open(file, 'r').readlines()

    length = len(things) -1         # number of items in dictionary (minus last entry -- other information)   
    keys = list(things)             # list of dictionary keys
    val_keys = []                   


    for i in range(length):         # format and print dict
        print(f"{keys[i]}:")
        val_dict = things[keys[i]]              # current nested dict
        val_keys = list(val_dict)               # list of nested dictionary keys
        for j in range(len(things[keys[i]])):
            print(f"\t{val_keys[j]}: {val_dict[val_keys[j]]}")      # print info / vals




#############################################################################################

### find, order, return dictionary of things
### ("channel", "clocktrack", "dma_central", "tmoip_system")
def get_things (word, file=dts):            # (search term, file)
    l = open(file, 'r').readlines()     # get lines by line number

    drivers = ["channel", "clocktrack", "dma_central", "tmoip_system"]      # this is doing nothing rn

    things = {}                         # dictionary of things to return
    # {<word><number order> : {<reg name 1> : <number/address>, <reg name 2> : <number/address>}}
    # ex (channel): {"ch0" : {"channel_in" : 0x800000, "channel_out" : 0x0302399, "line_test" : 0x0293443}}
    things_vals = []                    # list of nested dictionaries for things
    reg = []                            # nested lists of register numbers for each driver

    lines = get_lines(f"{word}@")               # get starting lines
    num_order = get_lines(f"{word}_number")     # get numbers for dictionary order
    length = len(lines)                         # number of dictionary items
    r_name = False                              # if register names found, set to true
    reg_name = []                               # register names (if exist)


    # get and format lines
    for i in range(length):                     # get number / order, registers, and reg names
        if num_order == [] or num_order == -1:          # if no order set -1 and keep order
            num_order = -1
        else:                                           # if numbers exist, format, get integers in dec
            num_order[i] = l[num_order[i]].replace(f"{word}_number = <", "").replace(">;", "").strip()
            num_order[i] = int(num_order[i], 0)

        for j in range(25):                             # get reg address line and reg names
            if lines[i] + j < len(l):                           # prevent line number out of range for end of file
                if '};' in l[lines[i] + j]:
                    break
                
                else:
                    if "reg-names" in l[lines[i] + j]:
                        reg_name.append(l[lines[i] + j])
                        r_name = True              
                
                    if "reg =" in l[lines[i] + j] and len(reg) < i + 1:     # 'and' prevents lines getting cut for some reason
                        reg.append(l[lines[i] + j].replace("reg = <", "").replace(">;", "").strip())


    # split reg lines and replace with necessary values
    for i in range(length):
        reg[i] = reg[i].split(" ")                  # split into list
        reg_num = len(reg[i])
        
        for j in range(reg_num):
            if len(reg[i][j]) >= len(max(reg[i], key=len)):         # get only longest items (address vals)
                reg[i].append(reg[i][j])
        
        del reg[i][0:reg_num]                       # remove old list items
    n = len(reg[0])                         # number of reg addresses for each


    # reg names and add to nested dictionaries
    for i in range(length):        
        
        if r_name == False:                             # if reg_name not exist --> reg_address1, 2, 3, ...
            reg_name.append([])
            for j in range(n):
                reg_name[i].append(f"reg_address_{j+1}")
        else:                                           # if exists --> format into names list
            reg_name[i] = reg_name[i].replace("reg-names = \"", "").replace("\";", "").replace("\\0", " ").strip()
            reg_name[i] = reg_name[i].split(" ")


    # create list of dictionaries for each
    for i in range(length):
        temp = {}                                   # add to temp dict
        for j in range(n):
            if type(reg_name[i]) == str:               # if no register names    
                temp[reg_name[i]] = reg[i][j]
            else:
                temp[reg_name[i][j]] = reg[i][j]

        things_vals.append(temp)                    # add dictionaries to list


    # format things dict
    for i in range(length):                         # get order and add to things dict

        if word == "clocktrack":
            word_thing = "clocktr"
        elif '_' in word:
            word_thing = word[0:word.index('_')]
        else:
            word_thing = word[0:2]

        if num_order == -1:                                 # if no order
            things[f"{word_thing}{i}"] = things_vals[i]

        else:                                               # if number order
            idx = num_order.index(min(num_order))                       # get min val        
            things[f"{word_thing}{num_order[idx]}"] = things_vals[idx]   # add smallest num_order key to dict with nested dict as value
            num_order[idx] = max(num_order) + 10                        # make min > max to 'remove'

    things[word] = word                             # last dict entry for other information (just keyword / search term for now)


    show_info(things)
    #return things
