# dash documentation & stuff:   https://dash.plotly.com/dash-core-components
# frameworks & web info:    https://www.educative.io/blog/web-development-in-python#frameworks
# dash example (githubl linked):    https://dash.gallery/dash-clustergram/
# dash html.P style references/examples:    https://www.programcreek.com/python/example/100614/dash_html_components.P

# http://127.0.0.1:8000/
# os.popen("<command>").read()

# this python script will be run on a raspberry pi 4
# it should be able to run a simple webserver to control
# the states of the pins (on/off, input/output) remotely

from dash import Dash, html, dcc, Input, Output
from raspi_lists import *

############################################    ---     CONSTANTS
ON = 'dh'
OFF = 'dl'

INPUT = 'ip'
OUTPUT = 'op'

### webserver
PORT = 8000
HOST = '127.0.0.1'              # dash defult

app = Dash(__name__)
############################################    ---     VARIABLES
pinout_top = 150
pinout_left = 180

# list of pins to auto check -- on/lvl 1, output, or not gpio
l_onpins = pin_auto_set()[0]
r_onpins = pin_auto_set()[1]

l_inpins = pin_auto_set()[2]
r_inpins = pin_auto_set()[3]

# list of pin states to display
left_state = pin_state('left')
right_state = pin_state('right')
############################################    ---     WEBSERVER

### WEBSERVER
app.layout = html.Div([                     # show stuff on webs server
    html.H2("RPI 4 GPIO stuff"),    # header
    html.Br(), html.Br(), html.Br(),

## HEADERS
    html.Div(       
        html.H3('pinout'),style={
            'top':pinout_top-100, 'left':pinout_left+90, 
            'position':'absolute', 'textAlign':'center'}
        ),
    html.Div(                       # on/off
        html.P('on/off'),style={
            'top':pinout_top-30, 'left':pinout_left+100, 
            'position':'absolute', 'textAlign':'center',
            #'writing-mode': 'vertical-lr', 'text-orientation': 'upright',
            'letter-spacing': '-0.5px'}
        ),
    html.Div(                       # left input
        html.P('output'),style={
            'top':pinout_top-40, 'left':pinout_left+60, 
            'position':'absolute', 'textAlign':'center',
            #'writing-mode': 'vertical-lr', 'text-orientation': 'upright',
            'letter-spacing': '-0.5px'}
    ),
    html.Div(                       # right input
        html.P('output'),style={
            'top':pinout_top-40, 'left':pinout_left+140, 
            'position':'absolute', 'textAlign':'center',
            #'writing-mode': 'vertical-lr', 'text-orientation': 'upright',
            'letter-spacing': '-0.5px'}
    ),

##  PINOUT 
    html.Div(           # pinout left side (odd numbers)
        left_disp, style={
            'top':pinout_top-9, 
            'left':pinout_left-5, 
            'position':'absolute', 
            'textAlign':'right', 
            'line-height':4}
            ),
    html.Div(           # pinout right side (even numbers)
        right_disp, style={
            'top':pinout_top-9, 
            'left':pinout_left+160, 
            'position':'absolute', 
            'line-height':4}
            ),
    
    html.Div(           # pin state left side (odd numbers)
        left_state, style={
            'top':pinout_top+7, 
            'left':pinout_left-115, 
            'position':'absolute', 
            'textAlign':'right', 
            'line-height':4,
            'color': 'red'}
            ),
    html.Div(           # pin state right side (even numbers)
        right_state, style={
            'top':pinout_top+39, 
            'left':pinout_left+250, 
            'position':'absolute', 
            'line-height':4,
            'color': 'red'}
            ),

## ON / OFF
    html.Div([          # pinout left side (odd dumbers)
        dcc.Checklist(
            options=left_checks, value=l_onpins, inline=False, id='left_onoff_checks', 
            labelStyle = dict(display='block')      # not inline
        ),
        html.Div(id='left_onoff')
    ], style={'top':pinout_top, 'left':pinout_left+100, 'position':'absolute', 'textAlign':'right'}),

    html.Div([          # pinout right side (even numbers)
        dcc.Checklist(
            options=right_checks, value=r_onpins, inline=False, id='right_onoff_checks',
            labelStyle = dict(display='block')      # not inline
        ),
        html.Div(id='right_onoff')
    ], style={'top':pinout_top, 'left':pinout_left+120, 'position':'absolute'}),


## INPUT / OUTPUT
    html.Div([          # pinout left side (odd dumbers)
        dcc.Checklist(
            options=left_checks, value=l_inpins, inline=False, id='left_inout_checks', 
            labelStyle = dict(display='block')      # not inline
        ),
        html.Div(id='left_inout')
    ], style={'top':pinout_top, 'left':pinout_left+80, 'position':'absolute', 'textAlign':'right'}),

    html.Div([          # pinout right side (even numbers)
        dcc.Checklist(
            options=right_checks, value=r_inpins, inline=False, id='right_inout_checks',
            labelStyle = dict(display='block')      # not inline
        ),
        html.Div(id='right_inout')
    ], style={'top':pinout_top, 'left':pinout_left+140, 'position':'absolute'})
])



### CALLBACKS
# on / off
@app.callback(
    Output(component_id='left_onoff', component_property='children'),
    Input(component_id='left_onoff_checks', component_property='value')
)
def left_onoff (input_value):
    set_lvl(input_value, 'left')

@app.callback(
    Output(component_id='right_onoff', component_property='children'),
    Input(component_id='right_onoff_checks', component_property='value')
)
def right_onoff (input_value):
    set_lvl(input_value, 'right')



# input / output
@app.callback(
    Output(component_id='left_inout', component_property='children'),
    Input(component_id='left_inout_checks', component_property='value')
)
def left_inout (input_value):
    set_func(input_value, 'left')

@app.callback(
    Output(component_id='right_inout', component_property='children'),
    Input(component_id='right_inout_checks', component_property='value')
)
def right_inout (input_value):
    set_func(input_value, 'right')

############################################    ---     MAIN

if __name__ == "__main__":
    app.run(debug=True, port=PORT, host=HOST)




