# Project: liteCTRL
# File: Class def for Motor object
#
# Created by: Johanna Shaw


from machine import Pin, Timer, ADC


# Notes:
#	Consider Adding an enable pin for the motor so that it doesn't overheat!

# to implement:
#	Stop
#	Moving by a set amount



class Motor:

    # Class Members:

    # Step is the value of the current positiion of the curtain interms of steps
    Step = 0
    # MaxStep is the total steps it takes to get the curtain to completely closed to completely open 
    MaxStep = 0
    # Moving holds the direction that the curtain is moving in
    # 1 = forwards (openning), 0 = stopped, -1 = backwards (closing)
    Moving = 0
    # StepCheck tells motor whether or not to check for step positionend case
    StepCheck = False

    def __init__(self, pinA, pinB, pinC, pinD, pinEnable, pinBarrier):
        
        # initialize the output Step pins
        # note: pins A and B are friends, and pins C and D are friends
        self.PinA = Pin(pinA, Pin.OUT)
        self.PinB = Pin(pinB, Pin.OUT)
        self.PinC = Pin(pinC, Pin.OUT)
        self.PinD = Pin(pinD, Pin.OUT)
        
        # Pin dedicated to enabling the motor  (So that the motor doesn't get super hot)
        self.EnablePin = Pin(pinEnable, Pin.OUT)

        # Pin that tells us whether or not we hit an edge
        self.BarPin = ADC(Pin(pinBarrier))
        # self.BarPin.read_u16()    # returns ADC value between 0 and 65535

        # initialize the timer
        self.Timer = Timer()


    def StartForward(self, frequency):        
        # set the initial motor values so they alternate
        if self.Step & 1 == 0:
            self.__set1()
        else:
            self.__set2()
        
        self.Start(frequency, 1)

        
    def StartBackward(self, frequency):
        # set the initial motor values so they alternate
        if self.Step & 1 == 0:
            self.__set2()
        else:
            self.__set1()
        
        self.Start(frequency, -1)

    # used for 
    def __set1(self):
        self.PinA.value(0)
        self.PinB.value(1)
        self.PinC.value(0)
        self.PinD.value(1)

    def __set2(self):
        self.PinA.value(1)
        self.PinB.value(0)
        self.PinC.value(0)
        self.PinD.value(1)

    # Helper function for StartBackwards and StartForwards
    def Start(self, frequency, direction):
        # Enable the motor and then start the timer
        self.EnablePin.value(1)

        self.Timer.init(freq=frequency, mode=Timer.PERIODIC, callback=self.MoveStep)

        if direction < -1 or direction > 1:
            raise ValueError("MotorSteps.Start : Variable 'direction' needs to be within range: [-1, 1]")

        self.Moving = direction


    # Stops the motor and makes it so that there's no electricity going through it
    def Stop(self):
        self.EnablePin.value(0)
        self.Timer.deinit()

        # Easy reference for whether or not the motor is currentlty running        
        self.Moving = 0

        # reset the Stepcheck value
        self.StepCheck = False


    # The Callback function driving each motor step
    # Uses a full-wave stepping pattern
    def MoveStep(self, timer):
        # if forward: Step += 1,
        # if backwards Step -= 1
        self.Step += self.Moving
        
        # if Step is an odd number (aka alternate between these two)
        if self.Step & 1 == 1:        
            self.PinC.toggle()
            self.PinD.toggle()
        else:
            self.PinA.toggle()
            self.PinB.toggle()
        
        # check for if we've stopped at the desired location
        if self.StepCheck and self.Step == self.StepTarget:
            self.Stop()


    # will fully open and then fully close the curtains in order to get the total steps value
    def Calibrate(self):
        pass


    # will completely open the curtains
    def Open(self):
        pass


    # will completely close the curtains
    def Close(self):
        pass


    # will move curtains to percent open
    def MoveToPercent(self, percent):
        # set desired position
        self.StepTarget = (self.MaxStep * percent) // 100
        
        # set stepcheck so that the pico checks and stops at the desired location.
        self.StepCheck = True
        pass
    


