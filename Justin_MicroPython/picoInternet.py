# 
# Pico internet connection protocol 
# February 27, 2023
#
# Sources:
# projects.raspberrypi.org

import network
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

#led = machine.Pin("LED", machine.Pin.OUT)

ssid = "Justin’s iPhone"
password = "deskmate"

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
        pico_led.toggle()
        sleep(1)
        
    # print Pico ip address
    ip = wlan.ifconfig()[0]
    print(f"Connected on: {ip}")
    return wlan
    

wlanConnection = connect()