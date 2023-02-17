#from machine import Pin, Timer, I2C, SoftI2C
from MotorSteps import Motor


ourMotor = None

# basic initializations
def Main():

    # # lets go for pins [24:27] (gp 18:21)
    ourMotor = Motor(18, 19, 20, 21)
    #ourMotor.StartForward(500)
    ourMotor.StartBackward(500)


    # TESTING I2C:
    # initialize the I2C channels
    #i2c = SoftI2C(Pin(5), Pin(4))
    
    #print(i2c.scan())





Main()
