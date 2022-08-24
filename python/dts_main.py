# temporary (?) file used for testing things for the dts file search and webserver stuff
# drivers: channel, clocktrack, dma_central, tmoip_system

from dts_search import *            # file with search, format, and display functions for dt.dts file
from dts_webshow import app, PORT, HOST

###################################################


if __name__ == "__main__":

    ### get dictionaries of info
    channel = get_things("channel")
    clocktrack = get_things("clocktrack")
    dma_central = get_things("dma_central")
    tmoip_system = get_things("tmoip_system")

    ### print things to terminal
    #show_things(channel)
    #show_things(clocktrack)
    #show_things(dma_central)
    #show_things(tmoip_system)


    ### start webserver
    app.run(debug=True, port=PORT, host=HOST)





