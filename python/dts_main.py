# temporary (?) file used for testing things for the dts file search and webserver stuff
# drivers: channel, clocktrack, dma_central, tmoip_system

from dts_search import *            # file with search, format, and display functions for dt.dts file
from dts_webshow import app, PORT, HOST
import dts_webshow as s

###################################################


if __name__ == "__main__":

    ### print things to terminal
    #show_things(s.channel)
    #show_things(s.clocktrack)
    #show_things(s.dma_central)
    #show_things(s.tmoip_system)


    ### start webserver
    app.run(debug=True, port=PORT, host=HOST)
