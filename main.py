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
# from LEDStrip import LED_Strip_PWM, Colour
import LEDStrip
import time


class Main:
    # basic initializations
    timrr = Timer()

    MC_Timer = Timer()  # The timer used for ADC positioning callbacks
    IsManual = False

    def __init__(self):

        print("Got to main")

        # initialize the Motor, sensors, and LEDs

        # self.MotorInit()
        self.SensorsInit()
        # self.PWM_Strip_Init()
        # self.ManCurtainPosInit()      # initialize the ADC curtain position pin:
        

        # self.ourMotor.Calibrate()
        # self.SensorsTest()
        
        # testing my colour converter
        if self.APDS is not None:

            l, c, R, G, B = self.APDS.GetCRGB()
            print(LEDStrip.ConvertSensorRGB(R, G, B))



    # Initializes the light strip object
    # This should be the only add on that doesn't risk failing
    def PWM_Strip_Init(self):

        # initialize strip
        # GPIO pins: 11, 12, 13  =  irl pin: 15, 16, 17
        # self.Strip = LEDStrip.LED_Strip_PWM(R_Pin=11, G_Pin=12, B_Pin=13)

        
        # lets go for pins [24:26] (gp 18:20)
        self.Strip = LEDStrip.LED_Strip_PWM(R_Pin=18, G_Pin=19, B_Pin=20)
        print('Light strip initialized')

      
    def MotorInit(self):       
        # lets go for pins [24:27] (gp 18:21)
        # enable pin is on GPIO 10, or pin 14 irl
        # ADCBarrier pin is on GPIO 28, or pin 34 irl
        # self.ourMotor = Motor(18, 19, 20, 21, pinEnable=10, pinADCBarrier=28)
        
        # lets go for pins [14:17] (gp 10:13)
        # enable pin is on GPIO 14, or irl pin 19 
        # ADCBarrier pin is on GPIO 26, or pin 31 irl
        self.ourMotor = Motor(14, 15, 16, 17, pinEnable=14, pinADCBarrier=26)


    # initializes the VEML, APDS, and thier shared I2C channel
    def SensorsInit(self):
        # GPIO pins 4 and 5 map to irl pins 6 and 7
        # base_i2c(SCL=5, SDA=4)      #initialize the I2C channel

        # GPIO pins 16 and 17 map to irl pins 21 and 22
        base_i2c(SCL=17, SDA=16)      #initialize the I2C channel
        
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
        
    
    # initializes the ADC pin used for manual curtain positioning
    # GPIO pin 28 = irl pin 34
    # GPIO pin 27 = irl pin 32
    def ManCurtainPosInit(self):
        self.MC_Timer = Timer()
        self.IsManual = False
        # Use this if we're working with 2 pin design:
    # GPIO pin 28 = irl pin 34
        self.IsManualPin = Pin(28, Pin.IN)
        self.IsManualPin.irq(handler=self.ManualModePinChange, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
        if self.IsManualPin.value() == 1:
            self.ADCTimerStart()


        # GPIO pin 27 == irl pin 32
        self.CurPosPin = ADC(Pin(27))


    # Called if the user has turned on/off the manual modepositioning switch
    def ManualModePinChange(self, pin):
        print(pin.value())

        # manual mode on
        if pin.value() == 1:
            # Stop the motor (if on, no effect if off)
            self.ourMotor.Stop()
            # Start the callback timer
            self.ADCTimerStart()
        # manual mode off
        else:
            self.MC_Timer.deinit()
            self.IsManual = False

    # A Helper function
    # Uused in ManCurtainPosInit and ManualModePinChange, keeps things consistant.
    def ADCTimerStart(self):
            # callback set for 10Hz or 0.1s
            self.MC_Timer.init(freq=1, mode=Timer.PERIODIC, callback=self.ADCCallback)
            self.IsManual = True


    def ADCCallback(self, timer):
        # increments of 10%
        increment = 10
        # number between 0 and 65535
        # these theoretically correspond with 0 - 3.3V
        ADCVal = self.CurPosPin.read_u16()

        # irl values = 200-300 , 65535

        # working with ADC range of 350 to 65350, convert to %
        # DesPerc = (ADCVal - 350) // 650
        DesPerc = ((((ADCVal - 350) // 650) + increment / 2) // increment) * increment
        if DesPerc < 0:
            DesPerc = 0
        elif DesPerc > 100:
            DesPerc = 100

        # get the current curtain position rounded to "increment" percent
        curPerc = (( self.ourMotor.GetTargetPosPercent() + increment / 2) // increment) * increment
        newPerc = -1

        if DesPerc != curPerc:
        # if DesPerc < curPerc - increment * 3/4 or DesPerc > curPerc + increment * 3/4:
        # if DesPerc < curPerc - increment * 3/4 or DesPerc > curPerc + increment * 3/4:
            # set the curtain position to the new rounded position
            newPerc = ((DesPerc + increment / 2) // increment) * increment
            self.ourMotor.MoveToPercent(newPerc)
        
        print(f'ADC ={ADCVal}, Percent = {DesPerc}, New Perc = {newPerc}, Target = {self.ourMotor.GetTargetPosPercent()}')


        

    def SensorsTest(self):
        self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.SensorDataCallback)


    def SensorDataCallback(self, PIN=None):
        # receive the colours
        if self.APDS is not None:
            lux_APDS, clear, red, green, blue = self.APDS.GetCRGB()

        # Get Lux
        if self.VEML is not None:
            lux_VEML = self.VEML.Get_Lux()

        # clear1 = (clear + 500) / 2
        clear = (clear + 288) / 1.64
        # clear3 = (clear + 224) / 1.5

        
        #print(f'lux = {lux}, clear ={clear}, red = {red}, green = {green}, blue = {blue}')
        # print(f'{lux}, {clear1}, {clear2}, {clear3}')
        print(f'VEML = {lux_VEML}, APDS = {lux_APDS}')
        


if __name__ == '__main__':
    Main()
