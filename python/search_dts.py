from dts_search import get_lines
from dts_search import dts, txt, tst


#####################################################


def get_things (word, file):
    l = open(file, 'r').readlines()

    things = {}                 # main dict for things
    things_keys = []            # list of unordered keys
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


        # add to lists
        if "reg" in temp_keys and "reg-names" in temp_keys:
            # get index for vals
            # add together
            # delete keys and vals
        elif "reg" in temp_keys:
            #just add first
            #delete key and val
        
        lines = {}
        for j in range(len(temp_keys)):
            # add everything to lines as dictionary key and val
        

        # add lines as dict to things_vals



        lines, j = [], 0
