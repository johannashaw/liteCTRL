# Project: liteCTRL
# File: Class def for Motor object
#
# Created by: Johanna Shaw
# Edited:   
    # April 3, 2023 -- have code for calibrate, stop at barrier, and move to a set amount. Currently untested.


from machine import Pin, Timer, ADC
import time

# Notes:
#	Consider Adding an enable pin for the motor so that it doesn't overheat!

# to implement:
#	Stop
#	Moving by a set amount



class Motor:

    # Class Members:
    SaveFilename = 'Steps.txt'
    
    # MaxStep is the total steps it takes to get the curtain to completely closed to completely open 
    MaxStep = 112397

    # Step is the value of the current position of the curtain interms of steps
    CurrentStep = 112397
    StepTarget = CurrentStep
    
    # Moving holds the direction that the curtain is moving in
    # 1 = forwards (openning), 0 = stopped, -1 = backwards (closing)
    Moving = 0
    # StepCheck tells motor whether or not to check for step positionend case
    StepCheck = False

    # this indicates the value for openning.
    # it may change based on how the wires are hooked up
    forward = 1

    __calibrate = False
    MinFq = 500
    Frequency = MinFq
    MaxFq = 720

    lastBarrier = None

    def __init__(self, pinA, pinB, pinC, pinD, pinEnable, pinADCBarrier):
        
        # initialize the output Step pins
        # note: pins A and B are friends, and pins C and D are friends
        self.PinA = Pin(pinA, Pin.OUT)
        self.PinB = Pin(pinB, Pin.OUT)
        self.PinC = Pin(pinC, Pin.OUT)
        self.PinD = Pin(pinD, Pin.OUT)
        
        # Pin dedicated to enabling the motor  (So that the motor doesn't get super hot)
        self.EnablePin = Pin(pinEnable, Pin.OUT)

        # Pin that tells us whether or not we hit an edge
        self.BarPin = ADC(Pin(pinADCBarrier))
        # self.BarPin.read_u16()    # returns ADC value between 0 and 65535

        # initialize the timer
        self.Timer = Timer()

        # Get the saved steps from the last bootup
        self.ReadSteps()



    # Helper function for StartBackwards and StartForwards
    def __start(self, direction):
        if direction != 1 and direction != -1:
            raise ValueError(f'MotorSteps.__start : argument "direction" can only be 1 or -1, {direction} was given')
        
        # reset the frequency to the min
        self.Frequency = self.MinFq
        
        # Start position of motor pins A and B depend on position and whether Current Step is odd or even
        isforward = direction == 1          # true if forward
        iseven = self.CurrentStep & 1 == 0  # true if even
        if  isforward and iseven or not isforward and not iseven:
            self.PinA.value(1)
            self.PinB.value(0)
        else:
            self.PinA.value(0)
            self.PinB.value(1)

        # Pin C and D start at the same spot regardless of direction       
        self.PinC.value(0)
        self.PinD.value(1)

        # Enable the motor and then start the timer
        self.EnablePin.value(1)

        # start timer for callback function
        self.Timer.init(freq=self.Frequency, mode=Timer.PERIODIC, callback=self.__MoveStep)


        print(self.Frequency)

        self.Moving = direction


    # Stops the motor and makes it so that there's no electricity going through it
    def Stop(self):
        self.EnablePin.value(0)
        self.Timer.deinit()

        # Easy reference for whether or not the motor is currentlty running        
        self.Moving = 0

        self.StepTarget = self.CurrentStep

        # reset the Stepcheck value
        self.StepCheck = False

        self.Frequency = self.MinFq

        #save our new position.
        self.SaveSteps()

        # to give a small delay if the motor is changing directions
        time.sleep(0.001)


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
        if adcVal < 60000:
            # Stop moving
            if adcVal < 5000:
                # either both buttons are pressed or they are disconnected,
                # stop with error
                self.Stop()
                self.__calibrate = False
                print('Maybe tell the server so that the user can know the barriers are messed up')
                return
            # not sure if we want to do anything with this information
            elif adcVal < 25000 and self.Moving == -1: 
                # far/closed barrier is hit (470)                
                self.Stop()
                print('Closed barrier hit')
                print(f'ADC = {adcVal}\n')
            elif adcVal > 25000 and self.Moving == 1:
                # close/open barrier hit (1k)              
                self.Stop()
                print('Open barrier hit')
                print(f'ADC = {adcVal}\n')

            if self.__calibrate and self.Moving == 0:
                self.Calibrate()
                return

        # this will save the steps every rotation
        if self.CurrentStep % 200 == 0:     # and self.Frequency != self.MaxFq:
            self.SaveSteps()
            self.RampUpFreq()


    # will fully close and then fully open the curtains in order to get the total steps value
    def Calibrate(self):
        # self.__calibrate is used to indicate whether we're in the process of calibrating the curtain
        # self.__caliStep will hold our place in this function

        # Set Calibrating to true
        if self.__calibrate == False:
            self.__calibrate = True
            self.__caliStep = 1
        
        if self.__caliStep == 1:    
             # Start closing the curtain
            print('Calibrate Step 1\nStart closing the curtain')
            self.Close()
                
        elif self.__caliStep == 2: 
            # set CurentStep to 0
            # Start openning the curtain
            self.CurrentStep = 0
            print('Calibrate Step 2\nStart openning the curtain')
            self.Open()

        elif self.__caliStep == 3:        
            # Set Max-steps to CurrentStep
            # set Calibrating to false
            print('Calibrate Step 3')
            self.MaxStep = self.CurrentStep
            self.__calibrate = False
            print(f'New SaxSteps = {self.MaxStep}')

            # save the new steps to file 
            # (needs to do this again since the MaxStep may have changed)
            self.SaveSteps()
        
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
        print(f'moving to {percent}%')
        
        if self.StepTarget > self.CurrentStep:
            self.Open()
        elif self.StepTarget < self.CurrentStep:
            self.Close()
        else:
            self.StepCheck = False

        
        # do nothing if you're where you need to be


    # returns the current position of the curtain as a percent
    def GetCurrentPosPercent(self):
        return self.CurrentStep * 100 // self.MaxStep


    # returns the target position of the curtain as a percent
    def GetTargetPosPercent(self):
        return self.StepTarget * 100 // self.MaxStep
    
    
    #increases the Frequency that the motor is running at by 10Hz 
    def RampUpFreq(self):
        # check so don't do anything that you shouldn't be doing
        if self.Moving == 0 or self.Frequency == self.MaxFq:
            return
        self.Frequency += 10
        self.Timer.deinit()

        
        print(f'ramp = {self.Frequency}')

        self.Timer.init(freq=self.Frequency, mode=Timer.PERIODIC, callback=self.__MoveStep)


    # will save the current step position and the last recorded MaxStep value
    def SaveSteps(self):
        try:
            with open(self.SaveFilename, 'w', encoding='utf-8-sig') as file:
                file.write(f'{self.CurrentStep}\n')
                file.write(f'{self.MaxStep}')

        except Exception as ex:
            print(f'The given filename "{self.SaveFilename}" yielded an exception of type {type(ex)}')
            print(f'Exception was {ex}')
            print('Fhe Candidates and their weighted odds were not loaded')
            
            
    # reads the saved current step position and the last recorded maxstep value 
    # and then saves them to the corresponding class members 
    def ReadSteps(self):
        try:
            with open(self.SaveFilename, 'r', encoding='utf-8-sig') as file:
                try:
                    self.CurrentStep = int(file.readline())
                    self.MaxStep = int(file.readline())
                except:
                    print('Parsing the file did not work. WHOOPSIES!')

        except Exception as ex:
            print(f'The given filename "{self.SaveFilename}" yielded an exception of type {type(ex)}')
            print(f'Exception was {ex}')
        
        




