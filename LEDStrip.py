# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# Note: Still having issues with the GPIO input callback, fix later (?)

from machine import Pin
import time

# 0.0106
# 0.0128


# Designed for strip using WS2812B LEDs
class LEDStrip:

    # Maybe use the Enable pin, idk
    # LED strip has 60 pins, might reduce if needed
    def __init__(self, DataPin): #, EnablePin):

        # initialize GPIO pin that will be used for Data sent
        self.DataPin = Pin(DataPin, Pin.OUT)
        self.DataPin.value(0)

        # (maybe) initialize the Enable pin for the strip


    # Get a list of Colours, send them to the 
    def SetColours(self, Colrz):

        # iterate through the list of Colours
        for Col in Colrz:
            # make sure they don't fuck this up
            if type(Col) != Colour:
                raise TypeError("LEDStrip.LEDStrip.SetColours: an object in Colrz isn't of type Colour")
            # For each colour:
            for bitt in Col.GetAllBits():
                # set the high and low times
                if bitt == 0:
                    # 0 bit is  220ns~380ns high, 580ns~1µs low
                    high = 400 / 1000000000
                    low = 850 / 1000000000
                elif bitt == 1:
                    # 1 bit is  580ns~1µs high, 220ns~420ns low
                    high = 800 / 1000000000
                    low = 450 / 1000000000
                else:
                    print("Something messed up in LEDStrip")
                
                # send the bit to the light machine
                self.DataPin.value(1)
                time.sleep(high)
                self.DataPin.value(0)
                time.sleep(low)

                                
        # reset is low for >280µs
        self.DataPin.value(0)
             

    # this is meant to turn off all of the lights on the strip
    def Clear(self):
        pass


# Represents individual lights on the LED strip
class Colour:
    def __init__(self, Red, Green, Blue):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue


    # Used as an enumeration where it returns bits in order Green, Red, Blue, MSB first
    # Tested, looks good :)
    def GetAllBits(self):
        # return all of the bits for green
        for i in range(7, -1, -1):
            yield (self.Green >> i) & 1
        # return bits for red
        for i in range(7, -1, -1):
            yield (self.Red >> i) & 1
        # return bits for blue
        for i in range(7, -1, -1):
            yield (self.Blue >> i) & 1
        return

