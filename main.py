# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# Note: Still having issues with the GPIO input callback, fix later (?)

from machine import Pin, Timer, PWM, ADC
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

        self.timrr = Timer()

        print("Got to main")

        # # initialize the Motor, sensors, and LEDs
        # self.MotorInit()
        # self.SensorsInit()
        # self.PWM_Strip_Init()

        # initialize the ADC curtain position pin:
        self.ManCurtainPosInit()

        # forward = Pin(16, Pin.IN)
        # forward.irq(handler=self.OpenCallback, trigger=Pin.IRQ_RISING)

        
        # Backward = Pin(15, Pin.IN)
        # Backward.irq(handler=self.CloseCallback, trigger=Pin.IRQ_RISING)


    # initializes the ADC pin used for manual curtain positioning
    # if on, the 
    def ManCurtainPosInit(self):
        self.MC_Timer = Timer()
        self.IsManual = False
        # Use this if we're working with 2 pin design:
        # GPIO pin 16 = irl pin 21
        self.IsManualPin = Pin(16, Pin.IN)
        self.IsManualPin.irq(handler=self.ManualModePinChange, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
        if self.IsManualPin.value() == 1:
            self.ADCTimerStart()


        #gpio pin 27 == irl pin 32
        self.CurPosPin = ADC(Pin(27))


    def ManualModePinChange(self, pin):
        print(pin.value())

        # manual mode on
        if pin.value() == 1:
            self.ADCTimerStart()
        # manual mode off
        else:
            self.MC_Timer.deinit()
            self.IsManual = False

    # used in ManCurtainPosInit and ManualModePinChange, keeps things consistant.
    def ADCTimerStart(self):
            self.MC_Timer.init(freq=1, mode=Timer.PERIODIC, callback=self.ADCCallback)
            self.IsManual = True

    def ADCCallback(self, timer):
        # number between 0 and 65535
        # these theoretically correspond with 0 - 3.3V
        pinVal = self.CurPosPin.read_u16()

        # irl values = 200-300 , 65535
        print(pinVal)

    def OpenCallback(self, pin):           
        # GPIO pin 16
        print('openning')
        self.ourMotor.Open()
        
    def CloseCallback(self, pin):
        # GPIO piin 15
        print('closing')
        self.ourMotor.Close()

    # Initializes the light strip object
    # This should be the only add on that doesn't risk failing
    def PWM_Strip_Init(self):

        # initialize strip
        # GPIO pins: 11, 12, 13  =  irl pin: 15, 16, 17
        self.Strip = LED_Strip_PWM(R_Pin=11, G_Pin=12, B_Pin=13)
        print('Light strip initialized')

      
    def MotorInit(self):       
        # lets go for pins [24:27] (gp 18:21)
        # enable pin is on GPIO 10, or pin 14 irl
        # ADCBarrier pin is on GPIO 28, or pin 34 irl
        self.ourMotor = Motor(18, 19, 20, 21, pinEnable=10, pinADCBarrier=28)

        self.ourMotor.Frequency = 750

        self.ourMotor.Calibrate()


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
        

    def SensorDataCallback(self, PIN):
        # receive the colours
        if self.APDS is not None:
            clear, red, green, blue = self.APDS.GetCRGB()

        # Get Lux
        if self.VEML is not None:
            lux = self.VEML.Get_Lux()

        
        print(f'lux = {lux}, clear ={clear}, red = {red}, green = {green}, blue = {blue}')
        

    # Callback for VEML testing, prints LUX
    def printLUX(self, PIN):       
        print(self.VEML.Get_Lux())
       #  clear =565, red = 203, green = 148, blue = 151



if __name__ == '__main__':
    Main()
