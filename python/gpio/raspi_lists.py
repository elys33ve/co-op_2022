### functions for string and list manipulation stuff
# (not all of this is used, this script was just an attempt to organize stuff a bit while testing)

import os
from dash import html

############################################
"""
pininfo_get(pin) -- return lvl and func of pin

pinout_string() -- get str of just pins from pinout cmd output
pinout_labels() -- list of pin and gpio numbers to display
pinout_gpio() -- list of gpio numbers
pinout_disp() -- list of pin labels to display using html.P()
checkbox_list() -- list of dictionaries for checkboxes

set_lvl(pins, lr) -- set pin output levels (on/off)
set_func(pins, lr) -- set pin functions (input/output)
pin_auto_set() -- get all pins func and lvl to auto check correct boxes
pin_state(lr) -- list state of pins to display
"""
############################################    ---     constants
GPIO_PINS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']
NOT_GPIO_PINS = ['3V3', 'GND', '5V', '--']

ON = 'dh'
OFF = 'dl'

INPUT = 'ip'
OUTPUT = 'op'

ospinout = os.popen(f"pinout").read()

############################################    ---     usable functions

### GET INFO ABOUT PIN (LVL,FUNC)
def pininfo_get (pin):                           # get level, fsel, and function of pin
    
    if pin not in GPIO_PINS:    # if pin is not gpio pin
        return '-1', '-1'
    
    pininfo = os.popen(f"raspi-gpio get {pin}").read()
    lvl = pininfo[pininfo.index('level=') + 6]
    func = pininfo[pininfo.index('func=') + 5]

    if lvl == '0':      # get level (on/off)
        lvl = 'dl'
    elif lvl == '1':
        lvl = 'dh'

    if func == 'O':     # get function (input/output)
        func = OUTPUT
    elif func == 'I':
        func = INPUT

    return lvl, func


############################################    ---     STRING MANIPULATION / LISTS

### GET STRING OF PIN NUMBERS (FROM PINOUT)
def pinout_string ():
    idx1 = ospinout.index('J8:')
    idx2 = ospinout.index('POE:')

    pinout = ospinout[idx1:idx2-1].replace('J8:', '').strip()

    return pinout


### CREATE LIST OF PIN AND GPIO NUMBERS (together; to display)
def pinout_labels ():
    pinout = pinout_string().splitlines()    # list of pinout lines (two pins per)
    disp_pins = []      # list of all pins
    left_pins = []      # list of left pins (odd numbers)
    right_pins = []     # list of right pins (even numbers)

    for i in range(len(pinout)):
        idx = pinout[i].index(') (') + 1            # split line
        left_pin = pinout[i][:idx].strip()
        right_pin = pinout[i][idx:].strip()

        disp_pins.append(left_pin)      # add left side
        disp_pins.append(right_pin)     # add right side
        left_pins.append(left_pin)
        right_pins.append(right_pin)

    return disp_pins, left_pins, right_pins


### GET GPIO NUMS FOR PINS
def pinout_gpio ():
    disp_pins = pinout_labels()[0]
    gpio_list = []
    l_gpio = []
    r_gpio = []

    for i in range(len(disp_pins)):
        if "GPIO" in disp_pins[i]:          # gpio pins
            gpio = disp_pins[i].replace(f"({i+1})", "").replace("GPIO","").strip()
        elif "3V" in disp_pins[i]:          # 3v pins
            gpio = "3V3"
        elif "5V" in disp_pins[i]:          # 5v pins
            gpio = "5V"
        elif "GND" in disp_pins[i]:         # gnd pins
            gpio = "GND"
        else:                               # this shouldn't happen but eh
            gpio = "--"
        gpio_list.append(gpio)

    for i in range(len(gpio_list)):         # left and right lists
        if i%2 == 0:
            l_gpio.append(gpio_list[i])
        else:
            r_gpio.append(gpio_list[i])

    return gpio_list, l_gpio, r_gpio


### CREATE LISTS OF PIN LABELS TO DISPLAY
def pinout_disp ():              # pinout info for plain text
    left_labels = pinout_labels()[1]
    right_labels = pinout_labels()[2]
    l, r = [], []

    for i in range(len(left_labels)):
        l.append(html.P(left_labels[i]))
        r.append(html.P(right_labels[i]))

    return l, r


### CREATE TWO LISTS OF DICTIONARIES (RIGHT AND LEFT CHECKBOXES)
def checkbox_list ():           # pinout info for check boxes
    lgpio = pinout_gpio()[1]
    rgpio = pinout_gpio()[2]

    c1d = []
    c2d = []

    for i in range(len(lgpio)):
        if lgpio[i] in GPIO_PINS:
            c1d.append({'label':'','value':f'{lgpio[i]}'})
        else:
            c1d.append({'label':'','value':f'{lgpio[i]}', 'disabled':True})
        if rgpio[i] in GPIO_PINS:
            c2d.append({'label':'','value':f'{rgpio[i]}'})
        else:
            c2d.append({'label':'','value':f'{rgpio[i]}', 'disabled':True})

    return c1d, c2d


############################################ 

pinout_str = pinout_string()    # block string of pinout output

pin_labels, left_labels, right_labels = pinout_labels()     # lists of labels in 'GPIO# (#)' format

pin_gpio, left_gpio, right_gpio = pinout_gpio()     # lists of just gpio numbers in order of pinout

left_disp, right_disp = pinout_disp()       # lists of labels with html format to display

left_checks, right_checks = checkbox_list()     # list of dictionaries for checkboxes (blank txt output)







### TURN ON/OFF PIN(s)
def set_lvl (pins, lr):      # arg is list of gpio numbers (from input_value), right or left side
    if lr == 'left' or lr == 'l':
        gpio = left_gpio
    elif lr == 'right' or lr == 'r':
        gpio = right_gpio
    

    for i in range(len(gpio)):
        lvl = pininfo_get(gpio[i])[0]
        
        if gpio[i] in pins and lvl != '-1':    # if pin checkboxed and is gpio
            if lvl != ON:
                #print(f"turn on pin {gpio[i]} -- {lr} side")
                os.popen(f"raspi-gpio set {gpio[i]} dh")            # turn on
        elif gpio[i] not in pins and lvl != '-1':   # if pin not checkboxed and is gpio
            if lvl != OFF:
                #print(f"turn off pin {gpio[i]} -- {lr} side")
                os.popen(f"raspi-gpio set {gpio[i]} dl")            # turn off



### SET INPUT/OUTPUT PINS
def set_func (pins, lr):
    if lr == 'left' or lr == 'l':
        gpio = left_gpio
    elif lr == 'right' or lr == 'r':
        gpio = right_gpio

    for i in range(len(gpio)):
        func = pininfo_get(gpio[i])[1]
        
        if gpio[i] in pins and func != '-1':    # if pin checkboxed and is gpio
            if func == INPUT:
                #print(f"turn input pin {gpio[i]} -- {lr} side")
                os.popen(f"raspi-gpio set {gpio[i]} op")            # set output
        elif gpio[i] not in pins and func != '-1':   # if pin not checkboxed and is gpio
            if func == OUTPUT:
                #print(f"turn output pin {gpio[i]} -- {lr} side")
                os.popen(f"raspi-gpio set {gpio[i]} ip")            # set input




### CHECK PINS TO SET CHECK VALUE
def pin_auto_set ():
    l_onpins = ['3V3', 'GND']   # on/off -- pins that are on
    r_onpins = ['5V', 'GND']
    l_inpins = ['3V3', 'GND']   # in/out -- pins that are outputs
    r_inpins = ['5V', 'GND']

    for i in range(len(left_gpio)):
        lpin, rpin = left_gpio[i], right_gpio[i]

        lvl, func = pininfo_get(lpin)       # left side
        if lvl == ON:
            l_onpins.append(lpin)
        if func == OUTPUT:
            l_inpins.append(lpin)

        lvl, func = pininfo_get(rpin)       # right side
        if lvl == ON:
            r_onpins.append(rpin)
        if func == OUTPUT:
            r_inpins.append(rpin)
    
    return l_onpins, r_onpins, l_inpins, r_inpins



### CHECK PIN STATE FOR DISPLAY
def pin_state (lr):
    if lr == 'left' or lr == 'l':
        gpio = left_gpio
    elif lr == 'right' or lr == 'r':
        gpio = right_gpio

    states = []

    for i in range(len(gpio)):
        pin = gpio[i]
        lvl, func = pininfo_get(pin)

        if lvl == ON:       # set output words
            onoff = 'ON'
        else:
            onoff = 'OFF'
        if func == INPUT:
            inout = 'INPUT'
        else:
            inout = 'OUTPUT'

        if lvl != '-1':     # set/add output strings to list
            states.append(html.P(f"{inout} : {onoff}"))
        else:
            states.append(html.Br())       # skip if not gpio pin
        
    return states
        


