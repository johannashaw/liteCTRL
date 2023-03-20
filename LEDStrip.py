
from machine import Pin
import time


class LEDStrip:

    # Maybe use the Enable pin, idk
    # LED strip has 60 pins, might reduce if needed
    def __init__(self, DataPin): #, EnablePin):

        # initialize GPIO pin that will be used for Data sent
        self.DataPin = Pin(DataPin, Pin.Out)

        # (maybe) initialize the Enable pin for the strip


    # Get a list of Colours, send them to the 
    def SetColours(self, Colrz):

        # iterate through the list of Colours
        for Col in Colrz:
            # make sure they don't fuck this up
            if type(Col) != Colour:
                raise TypeError("LEDStrip.LEDStrip.SetColours: an object in Colrz isn't of type Colour")
            # For each colour:
            for bit in Col.GetAllBits():
                # set the high and low times
                match bit:
                    case 0:
                        # 0 bit is  220ns~380ns high, 580ns~1µs low
                        high = 270
                        low = 750
                    case 1:
                        # 1 bit is  580ns~1µs high, 220ns~420ns low
                        high = 750
                        low = 270
                
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


