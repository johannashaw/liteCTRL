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

def connect():
    #connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
