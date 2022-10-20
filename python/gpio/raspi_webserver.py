# dash documentation & stuff:   https://dash.plotly.com/dash-core-components
# frameworks & web info:    https://www.educative.io/blog/web-development-in-python#frameworks
# dash example (githubl linked):    https://dash.gallery/dash-clustergram/
# dash html.P style references/examples:    https://www.programcreek.com/python/example/100614/dash_html_components.P

# http://127.0.0.1:8000/

from dash import Dash, html, dcc, Input, Output
from things import SSH, pinout

############################################

PORT = 8000
HOST = '127.0.0.1'              # dash defult

app = Dash(__name__)

############################################    ---     CONSTANTS
ON = 'on'
OFF = 'off'

INPUT = 'ip'
OUTPUT = 'op'
############################################    ---     STRING MANIPULATION / LISTS

### GET STRING OF PIN NUMBERS
def pinout_parse (pinout):
    idx1 = pinout.index('J8:')
    idx2 = pinout.index('POE:')

    pinout = pinout[idx1:idx2-1]

    return pinout


### GET INFO ABOUT PIN (LVL,FUNC)
def get_pininfo (pin):                           # get level, fsel, and function of pin
    pininfo = "level=0 func=I"   ##### TEMP: CHANGE TO OS COMMAND: f"raspi-gpio get {pin}"
    lvl = pininfo[pininfo.index('level=') + 6]
    func = pininfo[pininfo.index('func=') + 5]

    if lvl == '0':          # for input and output
        lvl = 'dl'
    elif lvl == '1':
        lvl = 'dh'

    if func == 'O':
        func = OUTPUT
    elif func == 'I':
        func = INPUT

    return lvl, func


### CREATE LIST OF PIN AND GPIO NUMBERS
def pinout_list (pinout):
    pinout = pinout_parse(pinout).replace('J8:', '')
    pinout_keys = []
    tmp_list = [] 
    tmp = ''            # current word

    for i in range(len(pinout)):
        if pinout[i].isspace() == False:        # add letters/numbers until space
            tmp += pinout[i]
        elif pinout[i].isspace() == True and tmp != '':     # separate the gpio from (#) i guess
            pinout_keys.append(tmp)
            tmp = ''

    while len(pinout_keys) > 2:         # put the gpio/pin with (#) together and add to list
        pin = pinout_keys[0]+' '+pinout_keys[1]
        tmp_list.append(pin.strip())
        pinout_keys.remove(pinout_keys[0])
        pinout_keys.remove(pinout_keys[0])
    tmp_list.append(pinout_keys[0]+' '+pinout_keys[1])

    pinout_keys = tmp_list

    return pinout_keys


### GET GPIO NUMS FOR PINS
def gpio_nums ():
    pinout_keys = pinout_list(pinout)
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
keys = pinout_list(pinout)

### CREATE TWO LISTS OF PIN NUMBERS (RIGHT AND LEFT)
def pinout_txt (keys):              # pinout info for plain text
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
p1, p2 = pinout_txt(keys)           # right and left sides of pinout txt
############################################    ---     VARIABLES
pinout_top = 130
pinout_left = 150
############################################    ---     WEBSERVER

### WEBSERVER
app.layout = html.Div([                     # show stuff on webs server
    html.H2("RPI 4 GPIO stuff"),    # header
    html.Br(), html.Br(), html.Br(),

    html.Div(       
        html.H3('pinout'),style={
            'top':pinout_top-60, 'left':pinout_left+90, 
            'position':'absolute', 'textAlign':'center'}
        ),
    html.Div(
        html.P('On/Off'),style={
            'top':pinout_top-30, 'left':pinout_left+90, 
            'position':'absolute', 'textAlign':'center'}
    ),
    html.Div(           # pinout left side (odd numbers)
        p1, style={
            'top':pinout_top-9, 
            'left':pinout_left+15, 
            'position':'absolute', 
            'textAlign':'right', 
            'line-height':4}
            ),
    html.Div(           # pinout right side (even numbers)
        p2, style={
            'top':pinout_top-9, 
            'left':pinout_left+140, 
            'position':'absolute', 
            'line-height':4}
            ),


    html.Div([          # pinout left side (odd dumbers)
        dcc.Checklist(
            c1, inline=False, id='c1keys', 
            labelStyle = dict(display='block')      # not inline
        ),
        html.Div(id='info_out1')
    ], style={'top':pinout_top, 'left':pinout_left+100, 'position':'absolute', 'textAlign':'right'}),

    html.Div([          # pinout right side (even numbers)
        dcc.Checklist(
            c2, inline=False, id='c2keys',
            labelStyle = dict(display='block')      # not inline
        ),
        html.Div(id='info_out2')
    ], style={'top':pinout_top, 'left':pinout_left+120, 'position':'absolute'})
])



### CALLBACKS
@app.callback(
    Output(component_id='info_out1', component_property='children'),
    Input(component_id='c1keys', component_property='value')
)
def left_side (input_value):
    for i in range(len(input_value)):
        pinnum = input_value[i][input_value[i].index(':'+1):]
        lvl, func = get_pininfo(pinnum)
        print(f"pin {pinnum}, {lvl} {func}")
    return input_value

@app.callback(  
    Output(component_id='info_out2', component_property='children'),
    Input(component_id='c2keys', component_property='value')
)
def right_side (input_value):
    
    return 


############################################    ---     MAIN

if __name__ == "__main__":
    
    app.run(debug=True, port=PORT, host=HOST)
