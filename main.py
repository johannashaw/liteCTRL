# Project: liteCTRL
# File: Project's main file, starts the machine.
#       Is currently being used for testing 
#
# Created by: Johanna Shaw
# 
# Note: Still having issues with the GPIO input callback, fix later (?)

from machine import Pin, Timer, I2C, SoftI2C
from MotorSteps import Motor


ourMotor = None
# MGoBrr uses irl pin 32
MGoBrr = Pin(27, Pin.IN)
timrr = Timer()

# basic initializations
def Main():
    global ourMotor, MGoBrr, timrr

    print("Got to main")

    # MotorTesting()

    # TESTING I2C:
    # initialize the I2C channels
    # GPIO pins 4 and 5 map to irl pins 6 and 7
    i2c = I2C(id=0, scl=Pin(5, mode=Pin.ALT), sda=Pin(4, mode=Pin.ALT),  freq=400000)
    
    print(i2c.scan())
    print('done scanning')


def MotorTesting():       
    # lets go for pins [24:27] (gp 18:21)
    # enable pin is on GPIO 28, or pin 34 irl
    ourMotor = Motor(18, 19, 20, 21, 28)
    ourMotor.StartForward(500)
    # ourMotor.StartBackward(500)

    #MGoBrr.irq(handler=m_OnOff, wake=Pin.IDLE)#, trigger=Pin.IRQ_RISING)#, wake=machine.IDLE|machine.SLEEP)

    # Timer for testing start/stop functionality of the motor.
    timrr.init(freq=1, mode=Timer.PERIODIC, callback=m_OnOff)

# Used for testing motor library. Toggles motor between on and off using the enable pin.
def m_OnOff(PIN):
    global ourMotor

    print("I'm in.")

    if ourMotor.Started:
        ourMotor.Stop()
    else:
        # ourMotor.StartForward(500)
        ourMotor.StartBackward(500)



Main()
