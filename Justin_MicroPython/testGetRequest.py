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
#import micropython_urequests as requests

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
        print("Attempting connection...")
        pico_led.toggle()
        sleep(1)
        
    # print Pico ip address
    ip = wlan.ifconfig()[0]
    print(f"Connected on: {ip}")
    return ip

     
def GetRequest():
    testData = {"action" : "lightON"}
    response = urequests.get(
        "https://thor.cnt.sast.ca/~litectrl/webservice.php?device=motor&action=GoBrr")
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    response.close()
        
# try:
ip = connect()
    
    
# except KeyboardInterrupt:
#     print("resetting machine")
#     machine.reset()
  
counter = 0
while True:
        counter += 1
        print (f"Get Request #: {counter}")
        GetRequest()
        sleep(5)
        
