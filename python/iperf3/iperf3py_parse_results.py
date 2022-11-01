ifconfigtxt = "last_test.txt"



o = open(ifconfigtxt, 'r')
lines = o.readlines()

RX_packets, RX_bytes = 0, 0
RX_errors, RX_dropped, RX_overruns, RX_frame = 0, 0, 0, 0
TX_packets, TX_bytes = 0, 0
TX_errors, TX_dropped, TX_overruns, TX_carrier, TX_collisions = 0, 0, 0, 0, 0



for line in lines:
    if "RX packets" in line:                        # rx packets and bytes
        idx1 = line.index("RX packets") + 11
        idx2 = line.index("bytes") + 6
        idx3 = line.index(' (')

        a = int(line[idx1:idx2-6].strip())
        RX_packets += a
        b = int(line[idx2:idx3].strip())
        RX_bytes += b

    elif "RX errors" in line:                       # rx errors, dropped, overruns, frame
        idx1 = line.index("RX errors") + 10
        idx2 = line.index("dropped") + 8
        idx3 = line.index("overruns") + 9
        idx4 = line.index("frame") + 6

        a = int(line[idx1:idx2-8].strip())
        RX_errors += a
        b = int(line[idx2:idx3-9].strip())
        RX_dropped += b
        c = int(line[idx3:idx4-6].strip())
        RX_overruns += c
        d = int(line[idx4:].strip())
        RX_frame += d

    elif "TX packets" in line:                      # tx packets and bytes
        idx1 = line.index("TX packets") + 11
        idx2 = line.index("bytes") + 6
        idx3 = line.index(' (')

        a = int(line[idx1:idx2-6].strip())
        TX_packets += a
        b = int(line[idx2:idx3].strip())
        TX_bytes += b

    elif "TX errors" in line:                       # tx errors, dropped, overruns, carrier, collisions
        idx1 = line.index("TX errors") + 10
        idx2 = line.index("dropped") + 8
        idx3 = line.index("overruns") + 9
        idx4 = line.index("carrier") + 8
        idx5 = line.index("collisions") + 11

        a = int(line[idx1:idx2-8].strip())
        TX_errors += a
        b = int(line[idx2:idx3-9].strip())
        TX_dropped += b
        c = int(line[idx3:idx4-8].strip())
        TX_overruns += c
        d = int(line[idx4:idx5-11].strip())
        TX_carrier += d
        f = int(line[idx5:].strip())
        TX_collisions += f



print(f"RX packets= {RX_packets}")
print(f"RX bytes= {RX_bytes}")
print(f"RX errors= {RX_errors}")
print(f"RX dropped= {RX_dropped}")
print(f"RX overruns= {RX_overruns}")
print(f"RX frame= {RX_frame}")
print(f"TX packets= {TX_packets}")
print(f"TX bytes= {TX_bytes}")
print(f"TX errors= {TX_errors}")
print(f"TX dropped= {TX_dropped}")
print(f"TX overruns= {TX_overruns}")
print(f"TX carrier= {TX_carrier}")
print(f"TX collisions= {TX_collisions}")
