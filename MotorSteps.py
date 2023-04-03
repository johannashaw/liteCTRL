# Project: liteCTRL
# File: Class def for Motor object
#
# Created by: Johanna Shaw
# Edited:   
    # April 3, 2023 -- have code for calibrate, stop at barrier, and move to a set amount. Currently untested.


from machine import Pin, Timer, ADC


# Notes:
#	Consider Adding an enable pin for the motor so that it doesn't overheat!

# to implement:
#	Stop
#	Moving by a set amount



class Motor:

    # Class Members:

    # Step is the value of the current positiion of the curtain interms of steps
    CurrentStep = 0
    # MaxStep is the total steps it takes to get the curtain to completely closed to completely open 
    MaxStep = 0
    # Moving holds the direction that the curtain is moving in
    # 1 = forwards (openning), 0 = stopped, -1 = backwards (closing)
    Moving = 0
    # StepCheck tells motor whether or not to check for step positionend case
    StepCheck = False

    # this indicates the value for openning.
    # it may change based on how the wires are hooked up
    forward = 1

    __calibrate = False
    Frequency = 500

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



    # Helper function for StartBackwards and StartForwards
    def __start(self, direction):
        if direction != 1 or direction != -1:
            raise ValueError(f'MotorSteps.__start : argument "direction" can only be 1 or -1, {direction} was given')
        
        # Start position of motor pins A and B depend on position and whether Current Step is odd or even
        isforward = direction == 1          # true if forward
        iseven = self.CurrentStep & 1 == 0  # true if even
        if  isforward and iseven or not isforward and not iseven:
            self.PinA.value(0)
            self.PinB.value(1)
        else:
            self.PinA.value(1)
            self.PinB.value(0)

        # Pin C and D start at the same spot regardless of direction       
        self.PinC.value(0)
        self.PinD.value(1)

        # Enable the motor and then start the timer
        self.EnablePin.value(1)

        # start timer for callback function
        self.Timer.init(freq=self.Frequency, mode=Timer.PERIODIC, callback=self.__MoveStep)

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
    def __MoveStep(self, timer):
        # if forward: Step += 1,
        # if backwards Step -= 1
        self.CurrentStep += self.Moving
        
        # if Step is an odd number (aka alternate between these two)
        if self.CurrentStep & 1 == 1:        
            self.PinC.toggle()
            self.PinD.toggle()
        else:
            self.PinA.toggle()
            self.PinB.toggle()
        
        # check for if we've stopped at the desired location
        if self.StepCheck and self.CurrentStep == self.StepTarget:
            self.Stop()

        # check if a barrier has been hit
        adcVal = self.BarPin.read_u16()
        # one or both barrier buttons are pressed
        if adcVal < 65535 - 200:
            # Stop moving
            self.Stop()
            if adcVal < 65535/5:
                # either both buttons are pressed or they are disconnected,
                # stop with error
                self.__calibrate = False
                raise Exception('Maybe tell the server so that the user can know the barriers are messed up')
                return
            # not sure if we want to do anything with this information
            elif adcVal < 65535 / 2 - 200: 
                # far/closed barrier is hit
                pass
            else:
                # close/open barrier is hit
                pass

            if self.__calibrate == True:
                self.__calibrate()
        


    # will fully close and then fully close the curtains in order to get the total steps value
    def Calibrate(self):
        # self.__calibrate is used to indicate whether we're in the process of calibrating the curtain
        # self.__caliStep will hold our place in this function

        # Set Calibrating to true
        if self.__calibrate == False:
            self.__calibrate = True
            self.__caliStep = 1
        
        match (self.__caliStep):       
            case 1:
                 # Start closing the curtain
                self.Close()        
            case 2:
                # set CurentStep to 0
                # Start openning the curtain
                self.CurrentStep = 0
                self.Open()
            case 3:
                # Set Max-steps to CurrentStep
                # set Calibrating to false
                self.MaxStep = self.CurrentStep
                self.Calibrate = False
                print(f'New SaxSteps = {self.MaxStep}')
        
        self.__caliStep += 1

    
    # will completely open the curtains
    def Open(self):
        self.__start(1)


    # will completely close the curtains
    def Close(self):
        self.__start(-1)


    # will move curtains to percent open
    def MoveToPercent(self, percent):
        # set desired position
        self.StepTarget = (self.MaxStep * percent) // 100
        
        # set stepcheck so that the pico checks and stops at the desired location.
        self.StepCheck = True
        
        if self.StepTarget > self.CurrentStep:
            self.Open()
        elif self.StepTarget < self.CurrentStep:
            self.Close()
        
        # do nothing if you're where you need to be


