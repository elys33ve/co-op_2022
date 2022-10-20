### functions for string and list manipulation
from dash import Dash, html, dcc, Input, Output
from things import pinout as ospinout
from things import pininfo as ospininfo

### lists
GPIO_PINS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']
NOT_GPIO_PINS = ['3V3', 'GND', '5V', '--']

ON = 'on'
OFF = 'off'

INPUT = 'ip'
OUTPUT = 'op'

############################################    ---     usable functions

### GET INFO ABOUT PIN (LVL,FUNC)
def pininfo_get (pin):                           # get level, fsel, and function of pin
    pininfo = ospininfo           # f"raspi-gpio get {pin}"
    lvl = pininfo[pininfo.index('level=') + 6]
    func = pininfo[pininfo.index('func=') + 5]

    if lvl == '0':   
        lvl = 'dl'
    elif lvl == '1':
        lvl = 'dh'

    if func == 'O':
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
def pinout_list ():
    pinout = pinout_string()    # pinout block str
    disp_pins = []
    tmp_list = [] 
    tmp = ''                    # current word

    for i in range(len(pinout)):
        if pinout[i].isspace() == False:        # add letters/numbers until space
            tmp += pinout[i]
        elif pinout[i].isspace() == True and tmp != '':     # separate the gpio from (#) i guess
            disp_pins.append(tmp)
            tmp = ''

    while len(disp_pins) > 2:         # put the gpio/pin with (#) together and add to list
        pin = disp_pins[0]+' '+disp_pins[1]
        tmp_list.append(pin.strip())
        disp_pins.remove(disp_pins[0])
        disp_pins.remove(disp_pins[0])
    #tmp_list.append(pinout_keys[0]+' '+pinout_keys[1])

    disp_pins = tmp_list

    return disp_pins


### GET GPIO NUMS FOR PINS
def gpio_nums ():
    pinout_keys = pinout_list()
    gpio_list = []

    for i in range(len(pinout_keys)):
        if "GPIO" in pinout_keys[i]:
            gpio = pinout_keys[i].replace(f"({i+1})", "").replace("GPIO","").strip()
        elif "3V" in pinout_keys[i]:
            gpio = "3V3"
        elif "5V" in pinout_keys[i]:
            gpio = "5V"
        elif "GND" in pinout_keys[i]:
            gpio = "GND"
        else:
            gpio = "--"
        gpio_list.append(gpio)

    return gpio_list

############################################    ---     LISTS
"""
keys = pinout_list()

### CREATE TWO LISTS OF PIN NUMBERS (RIGHT AND LEFT)
def pinout_txt ():              # pinout info for plain text
    p1, p2 = [], []
    for i in range(len(keys)):
        if i%2 == 0:
            p1.append(html.P(keys[i]))
        else:
            p2.append(html.P(keys[i]))
    return p1, p2

### CREATE TWO LISTS OF DICTIONARIES (RIGHT AND LEFT CHECKBOXES)
def checkbox_list ():           # pinout info for check boxes
    gpionum = gpio_nums()
    c1d = []
    c2d = []
    for i in range(40):
        pinnum = i+1
        if i%2 == 0:
            c1d.append({'label':'','value':f'{pinnum}:{gpionum[i]}'})
        else:
            c2d.append({'label':'','value':f'{pinnum}:{gpionum[i]}'})
    return c1d, c2d


c1, c2 = checkbox_list()        # list of dictionaries for checkboxes (blank txt output)
p1, p2 = pinout_txt()           # right and left sides of pinout txt
"""
############################################ 

pinout_str = pinout_string()    # block string of pinout output

pinout_keys = pinout_list()


print(pinout_str)
print(pinout_keys)
