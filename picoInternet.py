# 
# Pico internet connection protocol 
# February 27, 2023
#
# Sources:
# projects.raspberrypi.org

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = "Name of wifi network"
password = "Wifi network password"

# function to connect to WLAN
# Sets up wlan object, activates the wireless,
# and provides ssid and password
def connect():
    #connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # attempt connection until successful
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
        
    # print Pico ip address
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip
    
# A socket is the way a server can listen for a
# client that wants to connect to it.
# In this case, the server is going to be the
# Raspberry Pi Pico W and the client will be a web
# browser on another computer.

# To open a socket, you need to provide the IP address
# and a port number. Port numbers are used by computers
# to identify where requests should be sent.
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

try:
    ip = connect()
    connection = open_socket(ip)
except KeyboardInterrupt:
    machine.reset()
