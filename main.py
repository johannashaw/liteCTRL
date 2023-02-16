from machine import Pin, Timer


tim = Timer()
state = 0

# set 4 pins as output
# lets go for pins [24:27] (gp 18:21)
MotorA = machine.Pin(18, Pin.OUT)
MotorB = machine.Pin(19, Pin.OUT)
MotorC = machine.Pin(20, Pin.OUT)
MotorD = machine.Pin(21, Pin.OUT)

# Indicator LED for when one rotation has been completed
RotIndLed = machine.Pin(0, Pin.OUT)


# basic initializations
def Main():
    StartMotor(500)
    
    # set the initial motor values so they alternate
    MotorA.value(0)
    MotorB.value(1)
    MotorC.value(0)
    MotorD.value(1)
    
    
def StartMotor(frequency):
    # initialize the timer
    tim.init(freq=frequency, mode=Timer.PERIODIC, callback=Step)
  

# The Callback function driving each motor step
# Uses a full-wave stepping pattern
def Step(timer):
    # remember that you need to state that it's global, THEN do something with it.
    global state
    state += 1
    
    if state & 1 == 1:        
        MotorC.toggle()
        MotorD.toggle()
    else:
        MotorA.toggle()
        MotorB.toggle()
    
    # If the motor has completed one full rotation
    if state % 200 == 0:
        state = 0
        FullRotation()


# One rotation has been completed
def FullRotation():
    RotIndLed.toggle()


Main()
