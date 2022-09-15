# functions for searching and displaying info from dts file
# eventually something like "dts-parser <file> <search str>" to do stuff

"""

(currently)
channel: registers/names, channel number, (clocks/names, bitrate, compatible, refclk, polarity c/d)
clocktrack: registers (en 0-3, setpoints (12), clocks/names, compatible)
dma_central: registers (clocks/names, interrupts/parent, retry, num channels, compatible)
tmoip_system: 

-----

get_lines(word)         # looks for str word in file, returns list of line numbers where it appears
get_things(driver)      # gets and formats all info for str driver, orders into and returns dict

show_lines(lines)       # prints all lines with lines as list/int for line number, or with search str
show_things()           # formats and prints dict of info from get_things()

"""


##### file stuff for testing
tst = "/home/fiona/projects/fi_src/python/test.txt"     # simplified dts file for testing
txt = "/home/fiona/Documents/test.txt"                  # txt file for testing stuff rn
dts = "/home/fiona/dt.dts"                              # the actual file


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



### search dts file for keyword (one of the 4 drivers specifically)
### create py dictionary for driver info
def get_things (driver, file=dts):
    l = open(file, 'r').readlines()

    things = {}                 # main dict for things
    things_vals = []            # list of unordered vals

    order = []                  # if theres pre-defined order

    start_lines = get_lines(f"{driver}@", file)
    amt = len(start_lines)
    i, j = 0, 0


    if len(start_lines) == 0:                   # prevent error if nothing found
        return {}


    ###     get start point
    for i in range(amt):
        if "{" in l[start_lines[i] + 1]:                    # normal ppl code
            start_lines[i] += 2
        elif "{" in l[start_lines[i]]:                      # semi-respectible ppl code
            start_lines[i] += 1
        else:                                               # no
            print("where tf is the curly thing")
            return 0


    ###     get lines
    for i in range(amt):
        lines = []                  # temp list for lines
        
        while "};" not in l[start_lines[i] + j]:        # get temp lines list
            lines.append(l[start_lines[i] + j].strip())
            j += 1

        temp_keys = []
        temp_vals = []
        for j in range(len(lines)):                     # get temp keys/vals lists
            
            # keys
            idx = lines[j].index("=")
            temp_keys.append(lines[j][0:idx].strip())
            lines[j] = lines[j].replace(f"{lines[j][0:idx]}= ", "")


            # vals
            lines[j] = lines[j].replace(";", "")

            if "\"" in lines[j]:                    # strings / names
                lines[j] = lines[j].replace("\"", "")
                if "\\0" in lines[j]:
                    tmp = []
                    while "\\0" in lines[j]:                    # multiple names
                        idx = lines[j].index("\\")
                        tmp.append(lines[j][0:idx])
                        lines[j] = lines[j].replace(f"{lines[j][0:idx]}\\0", "")
                    tmp.append(lines[j])
                    temp_vals.append(tmp)
                else:
                    temp_vals.append(lines[j])

            elif "<" in lines[j]:                   # numbers / addresses
                lines[j] = lines[j].replace("<", "").replace(">", "")
                temp_vals.append(lines[j])

        ## special things
        # (reg, reg-names, channel_number)
        if "reg" in temp_keys:                      # register addresses

            idx = temp_keys.index("reg")
            temp_vals[idx] = temp_vals[idx].split(" ")
            tmp = len(temp_vals[idx])
            
            for j in range(tmp):                            # get items w max str length
                if len(temp_vals[idx][j]) == len(max(temp_vals[idx], key=len)):
                    temp_vals[idx].append(temp_vals[idx][j])
            
            del temp_vals[idx][0:tmp]


        if "channel_number" in temp_keys:           # get order
            idx = temp_keys.index("channel_number")
            order.append(int(temp_vals[idx], 0))
            del temp_keys[idx]
            del temp_vals[idx]


        lines = {}                          # temp dictionary for sorting nodes

        ## add to temp dict 'lines'
        # specialer things for the top
        if "reg" in temp_keys and "reg-names" in temp_keys:     # if reg-names exists 
            idx_n = temp_keys.index("reg-names")
            idx_v = temp_keys.index("reg")
            nam = temp_vals[idx_n]
            reg = temp_vals[idx_v]

            for j in range(len(reg)):                               # add reg names / addresses to temp dict
                lines[nam[j]] = reg[j]

            del temp_keys[idx_n]                                    # delete from lists
            del temp_vals[idx_n]
            idx_v = temp_keys.index("reg")
            del temp_keys[idx_v]
            del temp_vals[idx_v]

        elif "reg" in temp_keys:                                # if only reg exists
            idx = temp_keys.index("reg")
            reg = temp_vals[idx]
            
            for j in range(len(reg)):                               # add reg addresses to front of dict
                lines[f"register_{j}"] = reg[j]

            del temp_keys[idx]                                      # delete from lists
            del temp_vals[idx]

        j = 0
        while f"en{j}" in temp_keys:                            # en0, en1, en...
            idx = temp_keys.index(f"en{j}")
            lines[temp_keys[idx]] = temp_vals[idx]
            del temp_keys[idx]
            del temp_vals[idx]
            j += 1

        to_remove = []                                          # i'm making this far more complicated than necessary                               
        for j in range(len(temp_keys)):                         # for setpoints
            if "setpoint" in temp_keys[j]:
                lines[temp_keys[j]] = temp_vals[j]
                to_remove.append(j)
        

        # add other things                          # - if i wanna make it even more unnecessarily complex,
        for j in range(len(temp_keys)):             # could sort by number found in temp_keys str -
            lines[temp_keys[j]] = temp_vals[j]
        

        things_vals.append(lines)                   # add dict to list of dict for each driver
        lines, j = [], 0                            # reset for next driver

    
    ### order
    for i in range(amt):                        # order and add nested dicts to main dict
        if order == []:
            things[f"{driver}{i}"] = things_vals[i]
        else:
            idx = order.index(min(order))
            things[f"{driver}{i}"] = things_vals[i]
            order[idx] = max(order) + 10


    return things


#############################################################################################


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



### print info from things dictionary
def show_things (things, file=dts):     # (dict of ordered driver info from funct get_things, file)
    if things == {}:                    # mostly for if fed from get_things, when word not found in file
        print("not found in file")              # avoid error
        return 0


    amt = len(things)
    keys = list(things)


    for i in range(amt):
        print("\n")
        print(f"{keys[i]}: ")                # driver name and number

        val_dict = things[keys[i]]
        val_keys = list(val_dict)

        for j in range(len(things[keys[i]])):       # print info from nested dictionaries

            if type(val_dict[val_keys[j]]) == list:         # to account for dumb unnecessary formating shit i may have done
                tmp = ""
                for k in range(len(val_dict[val_keys[j]]) - 1):
                    tmp += val_dict[val_keys[j]][k] + ", "
                tmp += val_dict[val_keys[j]][k + 1]
                print(f"\t{val_keys[j]}: {tmp}")

            else:
                print(f"\t{val_keys[j]}: {val_dict[val_keys[j]]}")

    print("\n\n")
