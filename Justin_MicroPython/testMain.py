# Mock main file to test import of my Web Utilities module

from PicoWebUtilities import *

Connect()

while True:
    systemData = CheckIn()
    print("-------")
    #print(type(systemData))
    print(systemData)
    print("-------")
    sleep(10)