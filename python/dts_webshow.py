# dash documentation & stuff:   https://dash.plotly.com/dash-core-components
# frameworks & web info:    https://www.educative.io/blog/web-development-in-python#frameworks

# http://127.0.0.1:8000/

# eventually will replace dts_webserver and index.html

from dash import Dash, html, dcc, Input, Output
import dash

############################################

PORT = 8000
HOST = '127.0.0.1'          # dash defult

app = Dash(__name__)

drivers = ['channel', 'clocktrack', 'dma_central', 'tmoip_system']

############################################

app.layout = html.Div([
    html.H4("dts thing"),
    html.Br(),
    html.Div([
        dcc.Dropdown(drivers, 'channel', id='my-input'),
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
        x=1
    elif input_value == drivers[1]:
        x=2
    elif input_value == drivers[2]:
        x=3
    elif input_value == drivers[3]:
        x=4

    return f'{x}'           ## return slider with however many numbers driver has (slider as ufunction)







if __name__ == '__main__':
    app.run(debug=True, port=PORT, host=HOST)
