# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# Note: Still having issues with the GPIO input callback, fix later (?)

from machine import Pin, Timer, I2C, SoftI2C, PWM
from MotorSteps import Motor
from I2C_Classes import base_i2c, VEML7700, APDS9960
from LEDStrip import WS2812B_Strip, LED_Strip_PWM, Colour
import time


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

        # # initialize the Motor, sensors, and LEDs
        # self.MotorInit()

        # self.SensorsInit()

        # self.WS2812B_Strip_Test()

        # pwm = PWM(Pin(11, mode=Pin.ALT))
        # pwm.freq(500)
        # pwm.duty_u16(5000)

        self.PWM_StripTest()

        # prints the data received from both sensors every second
        # self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.SensorDataCallback)


    # testing a strip that runs off of PWM
    def PWM_StripTest(self):

        # initialize strip
        # GPIO pins: 11, 12, 13  =  irl pin: 15, 16, 17
        self.Strip = LED_Strip_PWM(11, 12, 13)
        print('Light strip initialized')

        # pass a couple of different colour values
        #self.Strip.Set_Colour(Colour(255, 255, 255))
        self.Strip.Set_Colour(Colour(0, 0, 0))
        # self.Strip.Set_Colour(Colour())
        # self.Strip.Set_Colour(Colour())
        # self.Strip.Set_Colour(Colour())
        print('Colour Changed')

      
    def MotorInit(self):       

        # lets go for pins [24:27] (gp 18:21)
        # enable pin is on GPIO 28, or pin 34 irl
        self.ourMotor = Motor(18, 19, 20, 21, 28)

        # self.ourMotor.StartForward(500)
        # self.ourMotor.StartBackward(500)
        # self.MGoBrr.irq(handler=self.m_OnOff, wake=Pin.IDLE)#, trigger=Pin.IRQ_RISING)#, wake=machine.IDLE|machine.SLEEP)
        # Timer for testing start/stop functionality of the motor.
        # self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.m_OnOff)


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
        
        self.VEML.Get_Lux()
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
        

    def SensorDataCallback(self, PIN):
        # receive the colours
        if self.APDS is not None:
            clear, red, green, blue = self.APDS.GetCRGB()

        # Get Lux
        if self.VEML is not None:
            lux = self.VEML.Get_Lux()

        
        print(f'lux = {lux}, clear ={clear}, red = {red}, green = {green}, blue = {blue}')

    # This tests the LED strip
    def WS2812B_Strip_Test(self):
        
        # initialize the light strip object
        # GPIO in 13, maps to irl pin 17
        self.strip = WS2812B_Strip(13, 1)

        # # create the array of lights
        # lights = []
        # for i in range(60):
        #     lights.append(Colour(109, 0, 162))

        self.strip.SetColours(109, 0, 162, False)

        time.sleep(1)
        # send Colours
        self.strip.SendColours()

        print("Done Light Testing")

        self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.ColourSendTest)

    
    def ColourSendTest(self, PIN):
        
        self.strip.SendColours()
        

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
