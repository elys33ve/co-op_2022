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

############################################
channel = get_things("channel")
clocktrack = get_things("clocktrack")
dma_central = get_things("dma_central")
tmoip_system = get_things("tmoip_system")
############################################

def channel_rtn ():
    return 'channels (12)'

def clocktrack_rtn ():
    return 'clocktrack (3)'

def dma_central_rtn ():
    return 'dma_central (3)'

def tmoip_system_rtn ():
    return 'tmoip_system (0)'


app.layout = html.Div([
    html.H2("dts thing"),
    html.Br(),
    html.H4("Driver:"),
    html.Div([
        dcc.Dropdown(options=drivers, id='my-input'),
    ]),
    html.Br(),
    html.Div(id='my-output')
])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    if input_value == drivers[0]:
        return channel_rtn()
    elif input_value == drivers[1]:
        return clocktrack_rtn()
    elif input_value == drivers[2]:
        return dma_central_rtn()
    elif input_value == drivers[3]:
        return tmoip_system_rtn()

