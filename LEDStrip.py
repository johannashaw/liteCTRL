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
    def __init__(self, Red:int = 0, Green:int = 0, Blue:int = 0):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue

    def __iter__(self):
        self.iter = 0
        return self
    def __next__(self):
        # returns the RGB values
        if self.iter == 0:
            self.iter += 1
            return self.Red
        elif self.iter == 1:
            self.iter += 1
            return self.Green
        elif self.iter == 2:
            self.iter += 1
            return self.Blue
        
        raise StopIteration
    
    def __getitem__(self, item):
        # returns the RGB values
        if item == 0:
            return self.Red
        elif item == 1:
            return self.Green
        elif item == 2:
            return self.Blue
        
    def __setitem__(self, key, newvalue):
        # returns the RGB values
        if key == 0:
            self.Red = newvalue
        elif key == 1:
            self.Green = newvalue
        elif key == 2:
            self.Blue = newvalue

    
    # to initialize from another Colour
    def Copy(self, col):
        
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
    def Set(self, Red:int, Green:int, Blue:int):
        self.Red = Red
        self.Green = Green
        self.Blue = Blue

    # returns the RGB values in one call
    def get(self):
        return self.Red, self.Green, self.Blue 
    
    def NormalizeColour(self):
        # make sure that all components are positive
        smallest = min(self)
        if smallest < 0:
            for i in range(3):
                self[i] -= smallest		#since this is negative, this is like adding the absolute value of the smallest
                
        # find the largest value
        largestval = max(self)

        # print(f' colour = {self}, max = {largestval}')


        # use the largest value to normalize all of the colours
        for i in range(3):
            # print(self[i])
            self[i] = (self[i] * 255) // largestval
            # print(self[i])
        
        # return Color object with the normalized colour values
        return self


    
    
    def __str__(self) -> str:
        return f'[Red = {self.Red}, Green = {self.Green}, Blue = {self.Blue}]'
    
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
            col = Colour().Copy(o)
            col.Red = (col.Red + self.Red) // 2
            col.Green = (col.Green + self.Green) // 2
            col.Blue = (col.Blue + self.Blue) // 2

            return col
            


# takes in raw RGB values returned from the ADPS sensor and converts it into the standard 255 values
# returns a colour object
def ConvertSensorRGB(Red:int, Green:int, Blue:int):
    
    temp = [Red, Green, Blue]
    
    # print(f'ConvertSensorRGB : start = {temp}')

    # make sure that all of the values are positive
    smallest = min(temp)
    if smallest < 0:
        for i in range(3):
            temp[i] -= smallest		#since this is negative, this is like adding the absolute value of the smallest
            
    
    # print(f'ConvertSensorRGB : positive = {temp}')       

    # find the largest value
    largestval = max(temp)
    
    if largestval == 0:
        return Colour()


    # use the largest value to normalize all of the colours
    for i in range(3):
        temp[i] = (temp[i] * 255) // largestval

    
    # print(f'ConvertSensorRGB : normalized = {temp}')
    
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

    def __set(self):
            # Convert colour.Red to duty value / 1023
        # set duty cycle
        rdut = self.colour.Red * (65535 // 255)
        self.Red.duty_u16(rdut)

        # Convert colour.Green to duty value / 1023
        # set duty cycle
        gdut = self.colour.Green * (65535 // 255)
        self.Green.duty_u16(gdut)

        # Convert colour.Blue to duty value / 1023
        # set duty cycle
        bdut = self.colour.Blue * (65535 // 255)
        self.Blue.duty_u16(bdut)


    # Sets the Colour of the LED strip
    # Takes a Colour object as an argument, returns None
    def Set_Colour(self, colour:Colour):
        # raise error if colour is not type Colour
        if type(colour) is not Colour:
            raise TypeError(f"""LEDStrip.LED_Strip_PWM.Set_Colour : "colour" argument needs to be of type Colour, {type(colour)} was given""")

        #   as an unsigned 16-bit value in the range 0 (all off) to 65535 (all on) inclusive

        self.colour = colour

        self.__set()


        print(f'duty: red = {rdut}, green = {gdut}, blue = {bdut}')



    def AdjustAmbient(self, DesiredColour:Colour, sensor:APDS):
        
        # get the sensor colour
        l, c, r, g, b = sensor.GetCRGB()
    
        # get the sensor colour
        # r, g, b = 255, 128, 64

        # average out the components of both colours
        sens = Colour(r, g, b).NormalizeColour()

        DesiredColour.NormalizeColour()

        print(f'desired: {DesiredColour},\t sensor: {sens}')

        # newcol = Colour()

        temps = Colour()
        

        for i in range(3):
            temps[i] = DesiredColour[i]*2 - sens[i]

        # print(temps)
        
        newcol = temps.NormalizeColour()

        print (newcol)

    # takes in the string representation of a hex form colour, and uses it to set the light colours
    def SetFromHex(self, col):
        start = 1

        for i in range(3):
            print('0x' + col[start : start + 2])
            self.colour[i] = int('0x' + col[start : start + 2], 16)
            start += 2

        
        self.__set()


