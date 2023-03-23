# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# 

from machine import Pin
import time

# 0.0106
# 0.0128


# Designed for strip using WS2812B LEDs
class LEDStrip:

    # DataPin takes an int representing the GPIO pin that the data will be sent on
    # qtyLights is an int that is used to create the list of lights
    # LED strip has 60 pins, might reduce if needed
    def __init__(self, DataPin, qtyLights): #, EnablePin):

        # initialize GPIO pin that will be used for Data sent
        self.DataPin = Pin(DataPin, Pin.OUT)
        self.DataPin.value(0)

        # create the list of Lights of the size given by the user
        self.LED_list = []
        for i in range(qtyLights):
            self.LED_list.append(Colour())


    # Get a list of Colours, send them to the 
    def SendColours(self):

        # iterate through the list of Colours
        for Col in self.LED_list:

            # start the first high pulse
            self.DataPin.value(1)
            lastTick = time.ticks_cpu() 

            # For each colour:
            for bitt in Col.GetBits():
                #   Default system clock is 125MHz = 8[ns] period
                #   time.ticks_cpu() returns CPU ticks 
                #   time.ticks_diff(ticks1, ticks2)  accounts for signed values and wrap around, ticks1 - ticks2

                # send the bit to the light machine
                self.DataPin.value(1)

                # get the time spent high/low in terms of ticks per 8ns
                # time high for:    0 = 400ns,  1 = 800ns
                high = 50 + bitt * 50       # = 400e-9 + bitt * 400e-9 <== 
                # time low for:     0 = 850ns, 1 = 450ns
                low = 106 - bitt * 50      #  = 850e-9 - bitt * 400e-9 <== these are values per ns
                

                # time.sleep(high)
                while time.ticks_diff(time.ticks_cpu(), lastTick) < high:
                    pass    # makeshift sleep for ns
                lastTick = time.ticks_cpu() 
                
                self.DataPin.value(0)
                # time.sleep(low)
                while time.ticks_diff(time.ticks_cpu(), lastTick) < low:
                    pass    # makeshift sleep for ns
                lastTick = time.ticks_cpu() 

                                
        # reset is low for >280µs
        # reset indicates to the LED strip that the batch of data is done being sent.
        self.DataPin.value(0)
        time.sleep_us(280)
             

    # this is meant to turn off all of the lights on the strip
    def Clear(self):
        self.SetColours(0, 0, 0)

    # Sets all of the lights to the given colour
    # Will send the data once it is done by default, option to not
    def SetColours(self, Red, Green, Blue, send = True):

        # Go through light list changing each of the colours' RGB values to given RGB values
        for Col in self.LED_list:
            Col.Set(Red, Green, Blue)
        
        # send data te the strip
        if send:
            self.SendColours()
        


# Represents individual lights on the LED strip
class Colour:
    def __init__(self, Red = 0, Green = 0, Blue = 0):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue


    # Used as an enumeration where it returns bits in order Green, Red, Blue, MSB first
    # Tested, looks good :)
    def GetBits(self):
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


    # easy set of all the colours
    def Set(self, Red, Green, Blue):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue

    # returns the RGB values in one call
    def get(self):
        return self.Red, self.Green, self.Blue 

