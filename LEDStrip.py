# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# 

from machine import Pin, PWM
from I2C_Classes import APDS9960 as APDS
import time




# Represents individual lights on the LED strip
class Colour:
    # to initialize from ints
    def __init__(self, Red = 0, Green = 0, Blue = 0):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue

    # to initialize from another Colour
    def __init__(self, col):
        
        self.Red += col.Red
        self.Green += col.Green
        self.Blue += col.Blue


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
    
    def __str__(self) -> str:
        return f'Red = {self.Red}, Green = {self.Green}, Blue = {self.Blue}'
    
    def __eq__(self, o) -> bool:
        if type(o) is not Colour:
            return False
        
        return self.Red == o.Red and self.Green == o.Green and self.Blue == o.Blue
    
    def __add__(self, o):
        if type(o) is int:
            self.Red += o
            self.Green += o
            self.Blue += o
            return self
        if type(o) is Colour:
            col = Colour(o)
            col.Red = (col.Red + self.Red) // 2
            col.Green = (col.Green + self.Green) // 2
            col.Blue = (col.Blue + self.Blue) // 2

            return col
            


# takes in raw RGB values returned from the ADPS sensor and converts it into the standard 255 values
# returns a colour object
def ConvertSensorRGB(Red, Green, Blue):
    temp = [Red, Green, Blue]
    # find the largest value
    largestval = max(temp)

    # use the largest value to normalize all of the colours
    for i in range(3):
        temp[i] = (temp[i] * 255) // largestval
    
    # return Color object with the normalized colour values
    return Colour(temp[0], temp[1], temp[2])


# class to drive an LED strip where the colours are set by PWM 
class LED_Strip_PWM:
    # class variables
    freq = 500     # set frequency of all PWMs


    # Takes in 3 int arguments representing the GPIO pins for RGB PWMs
    # All PWMs are off by default (ie Colour(0, 0, 0) )
    def __init__(self, R_Pin, G_Pin, B_Pin):
        # set Red
        self.Red = self.__create_helper(R_Pin)
        # set Green
        self.Green = self.__create_helper(G_Pin)
        # set Blue PWN
        self.Blue = self.__create_helper(B_Pin)


        self.colour = Colour(0, 0, 0)


    # helps initialize the PWM pins. Sets frequency to default and duty to 0
    def __create_helper(self, pin):
        pwm = PWM(Pin(pin))
        pwm.freq(self.freq)
        pwm.duty_u16(0)

        return pwm


    # Sets the Colour of the LED strip
    # Takes a Colour object as an argument, returns None
    def Set_Colour(self, colour):
        # raise error if colour is not type Colour
        if type(colour) is not Colour:
            raise TypeError(f"""LEDStrip.LED_Strip_PWM.Set_Colour : "colour" argument needs to be of type Colour, {type(colour)} was given""")

        #   as an unsigned 16-bit value in the range 0 (all off) to 65535 (all on) inclusive

        # Convert colour.Red to duty value / 1023
        # set duty cycle
        rdut = colour.Red * (65535 // 255)
        self.Red.duty_u16(rdut)

        # Convert colour.Green to duty value / 1023
        # set duty cycle
        gdut = colour.Green * (65535 // 255)
        self.Green.duty_u16(gdut)

        # Convert colour.Blue to duty value / 1023
        # set duty cycle
        bdut = colour.Blue * (65535 // 255)
        self.Blue.duty_u16(bdut)

        print(f'duty: red = {rdut}, green = {gdut}, blue = {bdut}')

        self.colour = colour


    def AdjustAmbient(self, DesiredColour:Colour, sensor:APDS):
        
        # get the sensor colour
        l, c, r, g, b = sensor.GetCRGB()

        # average out the components of both colours
        newPWM = ConvertSensorRGB(r, g, b) + DesiredColour

        # 
        """            Color c1 = label2.BackColor;
            Color c2 = label3.BackColor;

            int[] rgb = {(c1.R + c2.R)/2, (c1.G + c2.G) / 2 , (c1.B + c2.B) / 2 };


            label5.BackColor = Color.FromArgb(rgb[0], rgb[1], rgb[2]);

            while (rgb.Max() < 255)
            {
                for (int i = 0; i < rgb.Length; i++)
                {
                    rgb[i]++;
                }
            }

            label4.BackColor = Color.FromArgb(rgb[0], rgb[1], rgb[2]);"""


# Designed for strip using WS2812B LEDs
class WS2812B_Strip:

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
        
