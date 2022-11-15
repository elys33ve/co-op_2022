# binho SPI for raspberry pi test
"""
i have no idea what im doing yet

- connect to binho device
- send data to pi with spi
- receive and read data from pi

- set gpio pin to input
- get pin value
- set gpio pin to output
- set output value high/low


pinout:    
IO4, SDI (9)(10) GND
IO3, SCK (7)(8)  VBUS
IO2, SDO (5)(6)  GND
IO1, CS1 (3)(4)  3V3
IO0, CS0 (1)(2)  GND

cs low - miso
cs high - mosi
"""

import sys, errno
from serial import SerialException
from binho.errors import DeviceNotFoundError

from binho import binhoHostAdapter
from time import sleep
###########################
"""
sdi - io4 - gpio10 (green)
clk - io3 - gpio11 (blue)
sdo - io2 - gpio09 (purple)
io - io1 - gpio12 (red)
cs - io0 - gpio21 (black) / ceo gpio07

gnd - gnd
3v3 - gpio26
"""

x = 100
y = 75
########################### capture connection errors
targetComport = "COM3"
binho1 = "0XF96EEEFA50573539382E3120FF092240"
binho2 = "0X270EBA6E50573539382E3120FF0C0832"
port1 = "/dev/ttyACM1"
port2 = "/dev/ttyACM0"
try:
    binho = binhoHostAdapter(port=port2)      # grab the first device found the system finds (or binho = binhoHostAdapter(deviceID = targetDeviceID))
except SerialException:
    print("Binho host adapter was found, but failed to connect bc another application is already connected to it.", file=sys.stderr)
    print("Please close the connection in the other application and try again.", file=sys.stderr)
    sys.exit(errno.ENODEV)
except DeviceNotFoundError:
    print(f"No Binho host adapter found on serial port '{targetComport}'.", file=sys.stderr)
    sys.exit(errno.ENODEV)

##########################



### SPI
def start_spi ():
    # cs -- io
    binho.operationMode = "SPI"     # set host adapter operationMode to 'SPI'

    cspin = binho.IO0       # cs pin - chip select

    binho.spi.mode = 1
    binho.spi.frequency = 6000000   # spi clock frequency, in Hz (500K, 800K, 1M, 2M, 3M, 4M, 6M, 8M, 12M, and 24M Hz)
    binho.spi.bitOrder = "LSB"          # bit order (MSB, LSB)
    binho.spi.bitsPerTransfer = 16      # bit transfer (8, 16)

    # clk -- io3
    clkpin = binho.IO3       # clk pin - clock
    # sdo -- io2
    sdopin = binho.IO2       # sdo pin - serial data out
    # sdi -- io4
    sdipin = binho.IO4       # sdo pin - serial data out

    return cspin


def cs (lvl):
    if lvl == 1:
        invert_cs = True
    else:
        invert_cs = False       # set active low signal (default)


def print_read (rxdata):
    # connect SDI and SDO signals together to create a loopback to see how data is received
    print(rxdata)
    rcvdBytes = "RxData:"   # print data in human friendly
    for byte in rxdata:
        rcvdBytes += "\t " + "0x{:02x}".format(byte)
    print(rcvdBytes)


def solid_color (red, green, blue):
    color = []
    for i in range(y):
        for j in range(x):
            color.append(red)
            color.append(green)
            color.append(blue)
    return color


if __name__ == "__main__":
    try:
        if binho.inBootloaderMode:
            print(f"{binho.productName} found on {binho.commPort}, but it cannot be used now because it's in DFU mode")
            sys.exit(errno.ENODEV)
        elif binho.inDAPLinkMode:
            print(f"{binho.productName} found on {binho.commPort}, but it cannot be used now because it's in DAPlink mode")
            print("Tip: Exit DAPLink mode using 'binho daplink -q' command")
            sys.exit(errno.ENODEV)
        else:
            print(f"Connected to a {binho.productName} (deviceID: {binho.deviceID}) on {binho.commPort}")

        cspin = start_spi()
        invert_cs = cs(0)       # cmd

        txData = [0xDE, 0xAD, 0xBE, 0xEF, 0xAD, 0xBE, 0xEF, 0xEF]       # bits to write to bus
        rxData = binho.spi.transfer(txData, 8, chip_select=cspin, invert_chip_select=invert_cs)     # data received/sent back to main

        print_read(rxData)
    finally:
        binho.close()       # close connection to host adapter
