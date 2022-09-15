# dash documentation & stuff:   https://dash.plotly.com/dash-core-components
# frameworks & web info:    https://www.educative.io/blog/web-development-in-python#frameworks
# dash example (githubl linked):    https://dash.gallery/dash-clustergram/
# dash html.P style references/examples:    https://www.programcreek.com/python/example/100614/dash_html_components.P

# http://127.0.0.1:8000/

from dash import Dash, html, dcc, Input, Output
from dts_search import get_things

############################################

PORT = 8000
HOST = '127.0.0.1'              # dash defult

app = Dash(__name__)

drivers = ['channel', 'clocktrack', 'dma_central', 'tmoip_system']

############################################
channel = get_things("channel")
clocktrack = get_things("clocktrack")
dma_central = get_things("dma_central")
tmoip_system = get_things("tmoip_system")
############################################

def format_things (driver, n, head):                # format output
    if driver == {}:                    # for if dict is empty (no info was found)
        return f'{driver} info unavailable.'

    keys = list(driver)             # list of dict keys
    val_dict = driver[keys[n]]      # list of dict vals
    val_keys = list(val_dict)       # list of keys for vals w type dict
    info_str = [head, html.Br()]    # list of strings to return

    for j in range(len(driver[keys[n]])):           # info from nested dictionaries
        if type(val_dict[val_keys[j]]) == list:         # to account for dumb unnecessary formating shit i may have done to dictionary
            tmp = ""
            for k in range(len(val_dict[val_keys[j]]) - 1):
                tmp += val_dict[val_keys[j]][k] + ", "
            tmp += val_dict[val_keys[j]][k + 1]
            info_str.append(html.P(f"{val_keys[j]}: {tmp}", style={'marginLeft':'3%'}))
        else:
            info_str.append(html.P(f"{val_keys[j]}: {val_dict[val_keys[j]]}", style={'marginLeft':'3%'}))

    return info_str

############################################


def get_labels (n):         # list of dictionaries (labels and values) for dropdown
    labels = []
    drop_list = []
    range_list = list(range(len(get_things(drivers[n]))))

    for i in range(len(get_things(drivers[n]))):
        labels.append(f'{drivers[n]} {range_list[i]}')
        drop_list.append({'label' : labels[i], 'value' : labels[i]})
    return drop_list


def smms (n):               # slider min max step
    mn = 0
    if len(get_things(drivers[n])) == 0:
        mx = 0
    else:
        mx = len(get_things(drivers[n])) - 1        # get length of dict for slider range
    sp = 1
    return mn, mx, sp



app.layout = html.Div([                     # show stuff on webs server
    html.H2("dts thing"), html.Br(),
    html.H4("Drivers:"),
    html.Div([
        dcc.Tabs(id='drivers_tabs', value='tab-1', children=[
            dcc.Tab(label=drivers[0], value='tab-1', id='channel_tab', children=[
                html.Br(),
                #dcc.Dropdown(options=get_labels(0), value=f'{drivers[0]} {0}', id='channel_drop')
                dcc.Slider(min=smms(0)[0],max=smms(0)[1], step=smms(0)[2], value=0, id='channel_slide'),
                html.Br(), html.Br(), html.Br(), 
                html.Div(id='info_out1')
            ]),
            dcc.Tab(label=drivers[1], value='tab-2', id='clocktrack_tab', children=[
                html.Br(),
                #dcc.Dropdown(options=get_labels(1), value=f'{drivers[1]} {1}', id='clocktrack_drop')
                dcc.Slider(min=smms(1)[0],max=smms(1)[1], step=smms(1)[2], value=0, id='clocktrack_slide'),
                html.Br(), html.Br(), html.Br(),
                html.Div(id='info_out2')
            ]),
            dcc.Tab(label=drivers[2], value='tab-3', id='dma_tab', children=[
                html.Br(),
                #dcc.Dropdown(options=get_labels(2), value=f'{drivers[2]} {2}', id='dma_drop')
                dcc.Slider(min=smms(2)[0],max=smms(2)[1], step=smms(2)[2], value=0, id='dma_slide'),
                html.Br(), html.Br(), html.Br(),
                html.Div(id='info_out3') 
            ]),
            dcc.Tab(label=drivers[3], value='tab-4', id='tmoip_tab', children=[
                html.Br(),
                #dcc.Dropdown(options=get_labels(3), value=f'{drivers[3]} {3}', id='tmoip_drop')
                dcc.Slider(min=smms(3)[0],max=smms(3)[1], step=smms(3)[2], value=0, id='tmoip_slide'),
                html.Br(), html.Br(), html.Br(),
                html.Div(id='info_out4')
            ])
        ])
    ])
])



### channel
@app.callback(
    Output(component_id='info_out1', component_property='children'),
    Input(component_id='channel_slide', component_property='value')
)
def update_channel (input_value):
    driver, n = channel, 0
    info_head = html.H4(f'{drivers[n]} {input_value}:', style={'marginLeft':'1%'})

    return format_things(driver, input_value, info_head)

### clocktrack
@app.callback(
    Output(component_id='info_out2', component_property='children'),
    Input(component_id='clocktrack_slide', component_property='value')
)
def update_clocktrack (input_value):
    driver, n = clocktrack, 1
    info_head = html.H4(f'{drivers[n]} {input_value}:', style={'marginLeft':'1%'})

    return format_things(driver, input_value, info_head)

### dma_central
@app.callback (
    Output(component_id='info_out3', component_property='children'),
    Input(component_id='dma_slide', component_property='value')
)
def update_dma (input_value):
    driver, n = dma_central, 2
    info_head = html.H4(f'{drivers[n]} {input_value}:', style={'marginLeft':'1%'})

    return format_things(driver, input_value, info_head)

### tmoip_system
@app.callback(
    Output(component_id='info_out4', component_property='children'),
    Input(component_id='tmoip_slide', component_property='value')
)
def update_tmoip (input_value):
    driver, n = tmoip_system, 3
    info_head = html.H4(f'{drivers[n]} {input_value}:', style={'marginLeft':'1%'})

    return format_things(driver, input_value, info_head)

