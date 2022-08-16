from dts_search import get_lines
from dts_search import dts, txt, tst


#####################################################


def get_things (word, file=dts):
    l = open(file, 'r').readlines()

    things = {}                 # main dict for things
    things_vals = []            # list of unordered vals

    order = []                  # if theres pre-defined order

    start_lines = get_lines(f"{word}@", file)
    amt = len(start_lines)
    i, j = 0, 0

    if start_lines == []:                   # prevent error if nothing found
        return 0


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
                if " " in lines[j]:                                     # - possibly make separate funct later -
                    tmp = lines[j].split(" ")
                    temp_vals.append(tmp)
                else:
                    temp_vals.append(lines[j])

        # special things
        # (reg, reg-names, channel_number)
        if "reg" in temp_keys:                      # register addresses
            idx = temp_keys.index("reg")
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


        lines = {}

        # add to lists
        if "reg" in temp_keys and "reg-names" in temp_keys:     # if reg-names exists 
            idx_n = temp_keys.index("reg-names")
            idx_v = temp_keys.index("reg")
            nam = temp_vals[idx_n]
            reg = temp_vals[idx_v]


            for j in range(len(nam)):                           # add channel names / addresses to temp dict
                lines[nam[j]] = reg[j]

            del temp_keys[idx_n]                                # delete from lists
            del temp_vals[idx_n]
            idx_v = temp_keys.index("reg")
            del temp_keys[idx_v]
            del temp_vals[idx_v]

        for j in range(len(temp_keys)):
            lines[temp_keys[j]] = temp_vals[j]
        

        things_vals.append(lines)
        lines, j = [], 0

    
    ### order
    for i in range(amt):
        idx = order.index(min(order))
        things[f"{word}{i}"] = things_vals[i]
        order[idx] = max(order) + 10


    return things




def show_things (things, file=dts):             # print stuff
    l= open(file,'r').readlines()

    amt = len(things)
    keys = list(things)


    for i in range(amt):
        print(f"{keys[i]}:")
        
        val_dict = things[keys[i]]
        val_keys = list(val_dict)

        for j in range(len(things[keys[i]])):   
                print(f"\t{val_keys[j]}: {val_dict[val_keys[j]]}")
            

