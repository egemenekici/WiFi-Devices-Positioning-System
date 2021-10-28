# WiFi-Devices-Positioning
WiFi Devices Positioning System with Triangulation Algorithm. Three steps are needed to make this project work. The first of these steps is to place the sensors that will scan for WiFi devices in previously known locations in order to give the most accurate result for the triangulation algorithm, and initialize these locations to the wifi_positioning.py file. The second step is to put the sensors' WiFi card in monitor mode and perform a WiFi scan; Saving the distance results obtained from the WiFi scanning performed in this step into the output.txt files and automatically putting the cards in monitor mode are provided in the wifi_scanner.py scripts. The third step is to collect these three different output files on the main machine by communicating between the sensors (this communication is provided by queue for this project) and run the wifi_positioning.py script, the script combines the three data it has and creates a successful positioning for the devices with estimated distances.

# Dependencies
  1) Python Scapy Lib
  2) Monitor Mode WiFi Card
  3) Python Pandas Lib (For Printing the Output)
  4) Python SymPy Lib (For Calculation of Triangulation Algorithm)
  5) Intersensor Communication Method

SCAPY Installation
------------
To install the current released version by using pip3: 

    $ pip3 install Scapy

Can cloned the current development version in Github:

    $ git clone https://github.com/secdev/scapy.git 
    $ cd scapy
    $ sudo python setup.py install

PANDAS Installation
------------
It can also be installed by using pip:

    $ pip3 install pandas

MONITOR MODE
------------
	1) Let's start by checking for the interface name:  
		>sudo iwconfig  
	2) It shows the name of the interface "wlan0" and that it is in "Mode: Managed".

	3) To enable monitor mode you once again have to turn the interface off, change its mode, then bring it back up again:  
		>sudo ifconfig wlan0 down  
		>sudo iwconfig wlan0 mode monitor  
		>sudo ifconfig wlan0 up  
	4) Check that with the "iwconfig" that the mode is changed to Monitor.

	5) To return the interface to normal managed mode:  
		>sudo ifconfig wlan0 down  
		>sudo iwconfig wlan0 mode managed  
		>sudo ifconfig wlan0 up 
    
PANDAS Installation
------------
It can also be installed by using pip:

    $ sudo pip3 install sympy
    
DISTANCE CALCULATION
------------
  
By scanning a Wi-Fi traffic, your antenna will receive different signal power levels from different hosts, measured in dBm (decibel-meter). This power level can be converted into an approximate distance using some math based on the signal's frequency.  
The basic idea is the more strong the signal, the closer you're to the host and vice versa.  
Although the position of an electron can't be determined and neither its energy, this can be mathematically formalized using Free-space path loss logarithmic attenuation :


<p align="center">

  <img src="https://user-images.githubusercontent.com/56837694/130437467-2463bac2-7050-4a91-b3c2-571fca651fbe.png">

</p>


147.55 is the constant which depends on the units, in this case it will be megahertz and meters, with the associated constant equal to 27.55.  
If distance is to be calculated, the formula needs to be reversed as follows: 

<p align="center">

  <img src="https://user-images.githubusercontent.com/56837694/130411977-644661da-b291-454c-91ee-a6b3aca36df2.png">

</p>


1) f is the frequency of WiFi in MHz
2) dBm is the indicated power level (RSSI Signal Strength)
3) c is our FSPL constant (27.55)
