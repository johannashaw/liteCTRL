
from machine import Pin


class LEDStrip:

    # Maybe use the Enable pin, idk
    # LED strip has 60 pins, might reduce if needed
    def __init__(DataPin, EnablePin):

        # initialize GPIO pin that will be used for Data sent

        # (maybe) initialize the Enable pin for the strip
        pass

    def SetColours():

        # iterate through the list of Colours
        # For each:
            # send byte of Green
            # send byte of Red
            # send byte of Blue

        pass

    def Clear():
        pass


class Colour:
    def __init__(self, Red, Green, Blue):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue


