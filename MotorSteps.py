# File contains a Class def for the motor
#
from machine import Pin, Timer


# Notes:
#	Consider Adding an enable pin for the motor so that it doesn't overheat!

# to implement:
#	Stop
#	Moving by a set amount



class Motor:

    # class atributes
    # Indicator LED for when one rotation has been completed
    RotIndLed = Pin(0, Pin.OUT)

    def __init__(self, pinA, pinB, pinC, pinD):
        
        # initialize the pins
        # note: pins A and B are friends, and pins C and D are friends
        self.PinA = Pin(pinA, Pin.OUT)
        self.PinB = Pin(pinB, Pin.OUT)
        self.PinC = Pin(pinC, Pin.OUT)
        self.PinD = Pin(pinD, Pin.OUT)
        
        # initialize the timer
        self.Timer = Timer()
        self.State = 0


    def StartForward(self, frequency):        
        # set the initial motor values so they alternate
        self.PinA.value(0)
        self.PinB.value(1)
        self.PinC.value(0)
        self.PinD.value(1)
        
        self.Timer.init(freq=frequency, mode=Timer.PERIODIC, callback=self.Step)
        
    def StartBackward(self, frequency):
        # set the initial motor values so they alternate
        self.PinA.value(1)
        self.PinB.value(0)
        self.PinC.value(0)
        self.PinD.value(1)
        
        self.Timer.init(freq=frequency, mode=Timer.PERIODIC, callback=self.Step)

    # The Callback function driving each motor step
    # Uses a full-wave stepping pattern
    def Step(self, timer):
        # remember that you need to state that it's global, THEN do something with it.
        self.State += 1
        
        # if State is an odd number (aka alternate between these two)
        if self.State & 1 == 1:        
            self.PinC.toggle()
            self.PinD.toggle()
        else:
            self.PinA.toggle()
            self.PinB.toggle()
        
        # If the motor has completed one full rotation
        if self.State % 200 == 0:
            self.State = 0
            self.FullRotation()

    
    # One rotation has been completed
    def FullRotation(self):
        self.RotIndLed.toggle()
    

#ourMotor = Motor(18, 19, 20, 21)
#ourMotor.StartMotor(500)

