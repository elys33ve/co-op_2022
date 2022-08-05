# python time python time
# this is like a temp test file btw
# channel, clocktrack, tmoip_system, dma_central





from py_files import *
get_things("channel")




"""
things = {"ch0" : {"channel_in" : "0x080000", "channel_out" : "0x083020", "line_test" : "0x802200"},
    "ch1" : {"channel_in" : "0x080000", "channel_out" : "0x083020", "line_test" : "0x802200"},
    "ch2" : {"channel_in" : "0x080000", "channel_out" : "0x083020", "line_test" : "0x802200"}}

keys = list(things)
length = len(keys)


for i in range(length):
    print(f"{keys[i]}:")
    val_dict = things[keys[i]]
    val_keys = list(val_dict)

    for j in range(len(val_keys)):
        val = val_dict[val_keys[j]]
        print(f"\t{val_keys[j]}: {val}")
"""







""" 
### tests and stuff

this = ['0x08', '0x02', '0x0a', '0904', '0x06', '0993', '0x07', '0x09', '0x00', '0x0b', '0x05', '0x01']
that = []

for i in range(len(this)):
    if this[i][0:2] == "0x":
        print(int(this[i], 16))
    else:
        print('no hex')

#####

l = [["1","331","1","22","1","333","1","22","1","332","1","22"],["1","333","1","22","1","333","1","22","1","333","1","22"],["1","333","1","22","1","333","1","22","1","333","1","22"]]

for i in range(3):
    ll = len(l[i])
    for j in range(ll):
        if l[i][j] >= max(l[i], key=len):
            l[i].append(l[i][j])
    del l[i][0:ll]

print(l)

#####

this = {0:["1","2","3"],1:["1","9","3"],2:["1","2","3"]}

x = this[1][1]

print(x)
"""
