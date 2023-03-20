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
import urequests
import json

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
    
    
def GetRequest():
    response = urequests.get(
        "https://thor.cnt.sast.ca/~litectrl/webservice.php?checkin")
    print(f"Response status code: {response.status_code}")
    #print(f"Response text: {response.text}")
    return json.loads(response.text)
    response.close()
    

wlanConnection = connect()

counter = 0
while True:
        counter += 1
        print (f"Get Request #: {counter}")
        x = GetRequest()
        print(x[0])
        print(f"Operate : {x[0]["Operate"]}")
        print(f"Direction : {x[0]["Direction"]}")
        print(f"Steps : {x[0]["Steps"]}")
        sleep(5)