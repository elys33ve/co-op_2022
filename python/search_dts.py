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

    length = len(things)            # number of items in dictionary      
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

    things = {}                         # dictionary of things to return
    # {<word><number order> : {<reg name 1> : <number/address>, <reg name 2> : <number/address>}}
    # ex (channel): {"ch0" : {"channel_in" : 0x800000, "channel_out" : 0x0302399, "line_test" : 0x0293443}}
    things_vals = {}                    # nested dictionary for things
    reg = []                            # nested lists of register numbers for each driver

    lines = get_lines(f"{word}@")               # get starting lines
    num_order = get_lines(f"{word}_number")     # get numbers for dictionary order
    length = len(lines)                         # number of dictionary items
    reg_name = []                               # register names (if exist)


    # get and format lines
    for i in range(length):                     # get number / order, registers, and reg names
        if len(num_order) <= 0:                         # if no order, generate list 0 to length
            num_order[i] = i
        else:                                           # if numbers exist, format, get integers in dec
            num_order[i] = l[num_order[i]].replace(f"{word}_number = <", "").replace(">;", "").strip()
            num_order[i] = int(num_order[i], 0)

        for j in range(25):                             # get reg address line and reg names
            if lines[i] + j < len(l):                           # prevent line number out of range for end of file
                if "reg-names" in l[lines[i] +j]:
                    reg_name.append(l[lines[i] + j])                
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
        


    # reg names and add to nested dictionaries
    for i in range(length):        
        if len(reg_name) < len(reg):                          # if reg_name not exist --> reg_address1, 2, 3, ...
            for i in range(len(reg[i])):
                reg_name.append(f"reg_address{i}")
        else:                                           # if exists --> format into names list
            reg_name[i] = reg_name[i].replace("reg-names = \"", "").replace("\";", "").replace("\\0", " ").strip()
            reg_name[i] = reg_name[i].split(" ")


    # format things dict
    for i in range(length):                         # get order and add to things dict
        for j in range(len(reg[i])):
            things_vals[reg_name[i][j]] = reg[i][j]

        idx = num_order.index(min(num_order))                       # get min val        
        things[f"{word[0:2]}{num_order[idx]}"] = things_vals        # add smallest num_order key to dict with nested dict as value
        
        num_order[idx] = max(num_order) + 10                        # make min > max to 'remove'
        
    show_info(things)


#    return things
