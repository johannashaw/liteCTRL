from machine import Pin, Timer, I2C, SoftI2C
from MotorSteps import Motor


ourMotor = None
MGoBrr = Pin(27, Pin.IN)

# basic initializations
def Main():
    global ourMotor, MGoBrr

    # # lets go for pins [24:27] (gp 18:21)
    # enable pin is on GPIO 28, or pin 36 irl
    ourMotor = Motor(18, 19, 20, 21, 28)
    #ourMotor.StartForward(500)
    ourMotor.StartBackward(500)

    MGoBrr.irq(m_OnOff, Pin.IRQ_RISING)




    # TESTING I2C:
    # initialize the I2C channels
    #i2c = SoftI2C(Pin(5), Pin(4))
    
    #print(i2c.scan())


def m_OnOff(PIN):
    global ourMotor

    print("I'm in.")

    if ourMotor.Started:
        ourMotor.Stop()
    else:
        ourMotor.StartForward(500)



Main()
