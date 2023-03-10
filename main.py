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

        # MotorTesting()

        # GPIO pins 4 and 5 map to irl pins 6 and 7
        base_i2c(SCL=5, SDA=4)      #initialize the I2C channel
        self.VEML_Testing()
        self.APDS_Testing()



    def MotorTesting(self):       

        # lets go for pins [24:27] (gp 18:21)
        # enable pin is on GPIO 28, or pin 34 irl
        self.ourMotor = Motor(18, 19, 20, 21, 28)
        self.ourMotor.StartForward(500)
        # ourMotor.StartBackward(500)

        #MGoBrr.irq(handler=m_OnOff, wake=Pin.IDLE)#, trigger=Pin.IRQ_RISING)#, wake=machine.IDLE|machine.SLEEP)

        # Timer for testing start/stop functionality of the motor.
        self.timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.m_OnOff)


    def VEML_Testing(self):
        
        self.VEML = VEML7700()

        print('VEML init')
        
        # print(VEML.I2C_Read(4))		# 4 is the command code for reading Ambient light
        
        # # VEML.Get_Lux()
        # timrr.init(freq=1, mode=Timer.PERIODIC, callback=self.printLUX)


    def APDS_Testing(self):

        self.APDS = APDS9960()

        print('APDS init')


    # Callback for VEML testing, prints LUX
    def printLUX(self, PIN):       
        print(self.VEML.Get_Lux())



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
