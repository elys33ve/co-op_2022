# dash documentation & stuff:   https://dash.plotly.com/dash-core-components
# frameworks & web info:    https://www.educative.io/blog/web-development-in-python#frameworks
# dash example (githubl linked):    https://dash.gallery/dash-clustergram/

# http://127.0.0.1:8000/

from dash import Dash, html, dcc, Input, Output
import dash

from dts_search import get_things

############################################

PORT = 8000
HOST = '127.0.0.1'          # dash defult

app = Dash(__name__)

drivers = ['channel', 'clocktrack', 'dma_central', 'tmoip_system']

# slider min, max, step -- update with variables from drivers later
s_min = 0
s_max = 12
s_step = 1


############################################
channel = get_things("channel")
clocktrack = get_things("clocktrack")
dma_central = get_things("dma_central")
tmoip_system = get_things("tmoip_system")
############################################

def get_labels (d_num):
    labels = []
    drop_list = []
    range_list = list(range(len(d_num)))
    for i in range(len(get_things(drivers[d_num]))):
        labels.append(f'{drivers[d_num]} {range_list[i]}')
        drop_list.append({'label' : labels[i], 'value' : labels[i]})
    return drop_list


app.layout = html.Div([
    html.H2("dts thing"), html.Br(),
    html.H4("Driver:"),
    html.Div([
        dcc.Tabs(id='drivers_tabs', value='tab-1', children=[
            dcc.Tab(label=drivers[0], value='tab-1', children=[
                dcc.Dropdown(options=get_labels(0), value=f'{drivers[0]} {0}', id='channel_drop')
            ]),
        dcc.Tab(label=drivers[1], value='tab-2', children=[
                dcc.Dropdown(options=get_labels(1), value=f'{drivers[1]} {1}', id='clocktrack_drop')
            ]),
        dcc.Tab(label=drivers[2], value='tab-3', children=[
                dcc.Dropdown(options=get_labels(2), value=f'{drivers[2]} {2}', id='dma_drop')
            ]),
        dcc.Tab(label=drivers[3], value='tab-4', children=[
                dcc.Dropdown(options=get_labels(3), value=f'{drivers[3]} {3}', id='tmoip_drop')
            ])
        ])
    ])
])



###### figure out callbacks

@app.callback(
    Output(component_id='dropbox_out', component_property='children'),
    Input(component_id='drivers_tabs', component_property='value')
)
def update_output_div(value):
    if value == drivers[0]:
        return channel_rtn()
    elif value == drivers[1]:
        return clocktrack_rtn()
    elif value == drivers[2]:
        return dma_central_rtn()
    elif value == drivers[3]:
        return tmoip_system_rtn()
