# 
# --- Pico internet connection protocol  -----------------------------------------------------------
# 
# March 28, 2023
#
# Sources:
# projects.raspberrypi.org
#
# April 12, 2023
# This section needs to be fully tested to ensure it 
# is robust and easy to use via simple function calls

import network
from time import sleep
#from picozero import pico_temp_sensor, pico_led
import machine
import urequests
import json

# Connection indicator off
pico_led.off()

ssid = "Justin’s iPhone"
password = "deskmate"

# function to connect to WLAN
# Sets up wlan object, activates the wireless,
# and provides ssid and password
def Connect():
    #connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    connectCount = 0
    
    # attempt connection until successful
    while wlan.isconnected() == False:
        connectCount += 1
        print(f"{connectCount}-Attempting connection...")
        #pico_led.toggle()
        sleep(1)
        
    # Connection indicator on
    #pico_led.on()

    # print Pico ip address
    ip = wlan.ifconfig()[0]
    print(f"Connected on: {ip}")

    # return connection object
    return wlan

Connect()
     
# function for making get requests to our server
def GetRequest(**kwargs):

    httpURL = "https://thor.cnt.sast.ca/~litectrl/webservice.php?" 
    for key, value in kwargs.items():
         httpURL += key + "=" + value + "&"

    httpURL = httpURL[:-1]
    print(httpURL)
    
    response = urequests.get(httpURL)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    response.close()
        


        
# ------------------------------------------------------------------------------------------------

# --- Pico CheckIn -------------------------------------------------------------------------------
# 
# Function for Pico to check database for user control parameters
# Each call will need to return to Pico: SystemMode, Intensity, Temperature, Curtain, Colour

def CheckIn():
     
    httpURL = "https://thor.cnt.sast.ca/~litectrl/webservice.php?CheckIn" 
    
    response = urequests.get(httpURL)
    #print(f"Response status code: {response.status_code}")
    #print(f"Response text: {response.text}")
    rawDic = json.loads(response.text)
    
    response.close()

    refinedDic = {}
    refinedDic['SystemMode'] = rawDic['SystemMode']['Mode']
    refinedDic['LightIntensity'] = rawDic['LightIntensity']['Value']
    refinedDic['LightTemperature'] = rawDic['LightTemperature']['Value']
    refinedDic['CurtainPosition'] = rawDic['CurtainPosition']['Value']
    refinedDic['LEDColour'] = rawDic['LEDColour']['HEX']

    return refinedDic

    


# ------------------------------------------------------------------------------------------------

# --- Pico Done/Acknowledge ---------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------

# --- Pico DataPost ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------