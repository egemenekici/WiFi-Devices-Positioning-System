from scapy.all import *
from threading import Thread
import pandas
import time
import os

# initialize the networks dataframe that will contain all access points nearby.
networks = pandas.DataFrame(columns=["BSSID", "dBm_Signal", "Channel", "Crypto", "Distance", "SSID"])

# set the index BSSID (MAC address of the AP).
networks.set_index("BSSID", inplace=True)

global frequency

def callback(packet):
    if packet.haslayer(Dot11Beacon):

        # get the MAC address of the network.
        bssid = packet[Dot11].addr2

        # get the name of the network.
        ssid = packet[Dot11Elt].info.decode()

        # get the RSSI power.
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"

        # extract network stats.
        stats = packet[Dot11Beacon].network_stats()

        # get the channel of the AP.
        channel = stats.get("channel")

        # get the crypto.
        crypto = stats.get("crypto")

        # get the distance.
        global frequency

        if channel == 1:
            frequency = 2412
        elif channel == 2:
            frequency = 2417
        elif channel == 3:
            frequency = 2422
        elif channel == 4:
            frequency = 2427
        elif channel == 5:
            frequency = 2432
        elif channel == 6:
            frequency = 2437
        elif channel == 7:
            frequency = 2442
        elif channel == 8:
            frequency = 2447
        elif channel == 9:
            frequency = 2452
        elif channel == 10:
            frequency = 2457
        elif channel == 11:
            frequency = 2462
        elif channel == 12:
            frequency = 2467
        elif channel == 13:
            frequency = 2472
        elif channel == 14:
            frequency = 2477

        distance = math.pow(10,(27.55 - (20 * math.log10(frequency)) + math.fabs(dbm_signal)) / 20.0)
        short_distance = "%.3f" % distance

        # write sniffing data into txt file.
        with open('AP2_values.txt', 'a') as f:
            f.write(bssid + "-" + str(short_distance) + "-" + "\n")

        with open('AP2_values.txt') as f:
            lines = f.readlines()
        lines.sort()

        with open('AP2_values.txt', 'w') as f:
            for line in lines:
                f.write(line)

        # send sniffing data into data frame.
        networks.loc[bssid] = (dbm_signal, channel, crypto, short_distance, ssid)

def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(7)

def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")

        # switch channel from 1 to 14 each 0.5s.
        ch = ch % 14 + 1
        time.sleep(0.5)

if __name__ == "__main__":

    # turning WiFi card into monitor mode.
    os.system("sudo ifconfig wlan0 down")
    os.system("sudo iwconfig wlan0 mode monitor")
    os.system("sudo ifconfig wlan0 up")

    # interface name, check before using with iwconfig.
    interface = "wlan0"

    # start the thread that prints all the networks.
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()

    # start the channel changer.
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()

    # start sniffing.
    sniff(prn=callback, iface=interface)

    # distance estimation and send clear data to new txt file.
    with open('AP2_values.txt') as f:
        lines = f.readlines()

    lines.append("x" + "-" + "x" + "-" + "\n")

    counterforDistance = 1

    dist_count_array = []
    dist_pos_array = []

    max_value = None
    max_idx = None

    # sort and count for each WiFi devices's distance information.
    for n in range(len(lines)-1):

        compare = lines[n].split("-")
        compared = lines[n+1].split("-")

        if compare[0] == compared[0]:

            if compare[1] == compared[1]:
                counterforDistance += 1

            else:
                dist_count_array.append(counterforDistance)
                dist_pos_array.append(compare[1])
                counterforDistance = 1

        else:
            dist_count_array.append(counterforDistance)
            dist_pos_array.append(compare[1])
            counterforDistance = 1

            # treat the most returning data as distance for every WiFi device in the network. 
            for idx, num in enumerate(dist_count_array):
                if (max_value is None or num > max_value):
                    max_value = num
                    max_idx = idx

            # write these calculated data into new txt file.
            with open('AP2_clear_value.txt', 'a') as f:
                f.write(compare[0]+"-"+ dist_pos_array[max_idx]+"\n")

            print('Maximum value:', max_value, "At index: ", max_idx)

            print(dist_count_array)
            print(dist_pos_array)

            dist_count_array = []
            dist_pos_array = []
            max_value = None
            max_idx = None

