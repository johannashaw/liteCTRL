# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# Note: Still having issues with the GPIO input callback, fix later (?)

from machine import Pin, Timer, I2C, SoftI2C
from MotorSteps import Motor
from I2C_Classes import base_i2c, VEML7700, APDS9960
from LEDStrip import LEDStrip, Colour


# ourMotor = None
# # MGoBrr uses irl pin 32
# MGoBrr = Pin(27, Pin.IN)
# timrr = Timer()

class Main:
    # basic initializations

    def __init__(self):

        self.ourMotor = None
        # MGoBrr uses irl pin 32
        self.MGoBrr = Pin(27, Pin.IN)
        self.timrr = Timer()

        print("Got to main")

        self.MotorInit()

        self.SensorsInit()

        self.LightTesting()
    

    def MotorInit(self):       

        # lets go for pins [24:27] (gp 18:21)
        # enable pin is on GPIO 28, or pin 34 irl
        self.ourMotor = Motor(18, 19, 20, 21, 28)
        self.ourMotor.StartForward(500)
        # ourMotor.StartBackward(500)

        # self.MGoBrr.irq(handler=self.m_OnOff, wake=Pin.IDLE)#, trigger=Pin.IRQ_RISING)#, wake=machine.IDLE|machine.SLEEP)

        # Timer for testing start/stop functionality of the motor.
        self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.m_OnOff)


    # initializes the VEML, APDS, and thier shared I2C channel
    def SensorsInit(self):
        # GPIO pins 4 and 5 map to irl pins 6 and 7
        base_i2c(SCL=5, SDA=4)      #initialize the I2C channel
        
        self.VEMLInit()
        self.APDSInit()


    # VEML is the ambient light sensor
    def VEMLInit(self):
        # try to initialize the VEML, if not responding, variable is set to none and exits function
        try:
            self.VEML = VEML7700()
            print('VEML init')
        except Exception as err:
            self.VEML = None
            print(err)
            return
        
        # print(VEML.I2C_Read(4))		# 4 is the command code for reading Ambient light
        
        VEML.Get_Lux()
        # self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.printLUX)


    # APDS is the Colour light sensor
    def APDSInit(self):
        # try to initialize the APDS, if not responding, variable is set to none and exits function
        try:
            self.APDS = APDS9960()
            print('APDS init')
        except Exception as err:
            self.APDS = None
            print(err)
            return
        finally:
            pass

        self.APDS.GetCRGB()
        
        # self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.ColourTest)


    # This tests the LED strip
    def LightTesting(self):
        
        # initialize the light strip object
        # GPIO in 13, maps to irl pin 17
        self.strip = LEDStrip(13)

        # create the array of lights
        lights = []
        for i in range(60):
            lights[i] = Colour(109, 0, 162)

        # send Colours
        self.strip.SetColours(lights)

    
    def ColourTest(self, PIN):
        
        clear, red, green, blue = self.APDS.GetCRGB()
        # RGB = bytearray(b'9\x02\xcd\x00\x98\x00\x9c\x00'
        
        print(f'clear ={clear}, red = {red}, green = {green}, blue = {blue}')
        

    # Callback for VEML testing, prints LUX
    def printLUX(self, PIN):       
        print(self.VEML.Get_Lux())


       #  clear =565, red = 203, green = 148, blue = 151



    # Used for testing motor library. Toggles motor between on and off using the enable pin.
    def m_OnOff(self, PIN):
        print("I'm in.")

        if self.ourMotor.Started:
            self.ourMotor.Stop()
        else:
            # ourMotor.StartForward(500)
            self.ourMotor.StartBackward(500)



if __name__ == '__main__':
    Main()
