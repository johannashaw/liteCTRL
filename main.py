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
from LEDStrip import LED_Strip_PWM, Colour
import LEDStrip
import time
import PicoWebUtilities as WU
# import _thread
# import threading


class Main:
    # basic initializations
    timrr = Timer()

    MC_Timer = Timer()  # The timer used for ADC positioning callbacks
    IsManual = False
    
    # Sensors:
    VEML = None
    APDS = None

    # Lights:
    Strip = None

    # Motor:
    ourMotor = None
    LastLuxTarget = None

    def __init__(self):

        print("Got to main")

        # initialize the Motor, sensors, and LEDs

        self.MotorInit()
        self.SensorsInit()
        self.PWM_Strip_Init()
        self.ManCurtainPosInit()      # initialize the ADC curtain position pin:
        

        # self.ourMotor.Calibrate()
        # self.ourMotor.Open()
        # self.ourMotor.Close()

        # self.SensorsTest()
        # self.Strip.Set_Colour(Colour(255, 0, 0))
        # self.Strip.Set_Colour(Colour(0, 255, 0))
        # self.Strip.Set_Colour(Colour( 0, 0, 255))
        
        # testing my colour converter
        # if self.APDS is not None:
        #     time.sleep(0.5)
        #     l, c, R, G, B = self.APDS.GetCRGB()
        #     print(LEDStrip.ConvertSensorRGB(R, G, B))


        # KEEP THIS AT THE END! it is a continuous loop    
        self.WebShit()

        # threading alternative
        # _thread.start_new_thread(self.WebShit, (0,0))
        # print('Thread started:')


    # Initializes the light strip object
    # This should be the only add on that doesn't risk failing
    def PWM_Strip_Init(self):

        # initialize strip
        # GPIO pins: 11, 12, 13  =  irl pin: 15, 16, 17
        # self.Strip = LEDStrip.LED_Strip_PWM(R_Pin=11, G_Pin=12, B_Pin=13)

        
        # lets go for pins [24:26] (gp 18:20)
        self.Strip = LED_Strip_PWM(R_Pin=18, G_Pin=19, B_Pin=20)
        print('Light strip initialized')

      
    def MotorInit(self):       
        
        # lets go for pins  GPIO 10, 11, 12, 13, or irl [14:17]
        # enable pin is on GPIO 14, or irl pin 19 
        # ADCBarrier pin is on GPIO 26, or pin 31 irl
        self.ourMotor = Motor(10, 11, 12, 13, pinEnable=14, pinADCBarrier=26)


    # initializes the VEML, APDS, and thier shared I2C channel
    def SensorsInit(self):

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
        else :
            self.ADCTimerStop()


        # GPIO pin 27 == irl pin 32
        self.CurPosPin = ADC(Pin(27))


    # Called if the user has turned on/off the manual modepositioning switch
    def ManualModePinChange(self, pin):
        print(pin.value())
        self.ourMotor.Stop()

        # manual mode on
        if pin.value() == 1:
            # Stop the motor (if on, no effect if off)
            # Start the callback timer
            self.ADCTimerStart()
        # manual mode off
        else:
            # self.MC_Timer.deinit()
            self.ADCTimerStop()


    # A Helper function
    # Uused in ManCurtainPosInit and ManualModePinChange, keeps things consistant.
    def ADCTimerStart(self):
        # self.timrr.deinit()
        self.MC_Timer.deinit()

        # callback set for 10Hz or 0.1s
        self.MC_Timer.init(freq=1, mode=Timer.PERIODIC, callback=self.ADCCallback)
        self.IsManual = True


    def ADCTimerStop(self):
        self.MC_Timer.deinit()
        
        self.IsManual = False

        # self.MC_Timer.init(freq=1, mode=Timer.PERIODIC, callback=self.WebShit)

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


    # does get request and then does *something* with the data :)
    def WebShit(self, DC_1 = None, DC_2 = None):

        lastRequest = None
        Luxes = []
        Temps = []
        lastTime = time.ticks_ms()

        while True:
            time.sleep(1)
            # 
            if not self.IsManual:
                # get the Lux and Temp, add to arrays                
                if self.APDS is not None:
                    lux_APDS, clear, red, green, blue = self.APDS.GetCRGB()
                    Luxes.append(lux_APDS)
                    Temps.append(Colour(red, green, blue).NormalizeColour())

                dic = WU.CheckIn()

                # if there's been a change in values or it's been a minute
                if lastRequest != dic or time.ticks_diff(time.ticks_ms(), lastTime) > 10 * 1000:
                    lastTime = time.ticks_ms()
                    lastRequest = dic

                    # Pass the 
                    self.ParseWebDic(dic, Luxes, Temps)
                    Luxes.clear()
                    Temps.clear()

            else:
                lastTime = time.ticks_ms()
                lastRequest = None
                Luxes.clear()
                Temps.clear()

           

    def ParseWebDic(self, dic, Luxes, Temps):
        # don't bother if it's not a dictionary
        if type(dic) is not dict:
            print(f'Not a Dictionary : {dic}')
            return

        print(dic)
        
        # Automatic mode stuff
        if 'SystemMode' in dic and dic['SystemMode'] == 'automatic':
            print(f'1 it is {dic['SystemMode']}')

            # 'LightTemperature': 'warm'
            if 'LightTemperature' in dic:
                self.LightTemp_Stuff(dic['LightTemperature'])
            # 'LightIntensity': 'shade'



        # Custom mode stuff
        elif 'SystemMode' in dic and dic['SystemMode'] == 'custom':
            print(f'2 it is {dic['SystemMode']}')

            # 'CurtainPosition': '24'
            if 'CurtainPosition' in dic:
                perc = int(dic['CurtainPosition'])
                # only request a curtain position change if the position is different from where it's already going
                if self.ourMotor.GetTargetPosPercent() != perc:
                    self.ourMotor.MoveToPercent(perc)

            # 'LEDColour': '#554d80'
            if 'LEDColour' in dic: # and self.LastColour != dic['LEDColour']:
                # self.LastColour = 
                self.Strip.SetFromHex(dic['LEDColour'])


    def LightIntensity_Stuff(self, Intense):
        LuxIntensities = {'bright': 5000, 'cheery' : 2000, 'shady' : 1000, 'dim' : 500, 'gloomy': 50}

        if Intense in LuxIntensities:
            DesLux = LuxIntensities[Intense]
        # do nothing if the value is garbage.
        else:
            return

        if self.LastLuxTarget != DesLux:


            # DO A THING HERE, I'M TIRED AND FORGOT WHAT
            pass


    def LightTemp_Stuff(self, temp):
        # Dictionary containing the Colours corresponding to the desired light temperature
        tempColours = {'warmer': Colour(255, 165, 45), 'warm': Colour(255, 202, 128), 'neutral': Colour(255, 255, 255), 'cold': Colour(214, 228, 255), 'colder': Colour(168, 197, 255)}

        if temp in tempColours:
            DesiredColour = tempColours[temp]
        # do nothing if the value is garbage.
        else:
            return

        # AdjustAmbient(self, DesiredColour:Colour, sensor:APDS)
        if self.APDS is not None:
            self.Strip.AdjustAmbient(DesiredColour, self.APDS)     
        else:
            self.Strip.Set_Colour = DesiredColour



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
        

def AverageColours(ColDic:dict) -> Colour:
    retCol = Colour()

    # Add all of the colour components together
    for col in ColDic:
        retCol += col

    # Devide each colour component by the length of the dictionary
    for x in range[3]:
        retCol[x] /= len(ColDic)

    return retCol

if __name__ == '__main__':
    Main()
