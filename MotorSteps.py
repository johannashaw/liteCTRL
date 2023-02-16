from machine import Pin, Timer



class Motor:

    # class atributes
    # Indicator LED for when one rotation has been completed
    RotIndLed = machine.Pin(0, Pin.OUT)

    def __init__(self, pinA, pinB, pinC, pinD):
        
        # initialize the pins
        # note: pins A and B are friends, and pins C and D are friends
        self.PinA = machine.Pin(pinA, Pin.OUT)
        self.PinB = machine.Pin(pinB, Pin.OUT)
        self.PinC = machine.Pin(pinC, Pin.OUT)
        self.PinD = machine.Pin(pinD, Pin.OUT)

        # set the initial motor values so they alternate
        self.PinA.value(0)
        self.PinB.value(1)
        self.PinC.value(0)
        self.PinD.value(1)

        self.Timer = Timer()
        self.State = 0


    def StartMotor(self, frequency):
        # initialize the timer
        self.Timer.init(freq=frequency, mode=Timer.PERIODIC, callback=self.Step)
  

    # The Callback function driving each motor step
    # Uses a full-wave stepping pattern
    def Step(self, timer):
        # remember that you need to state that it's global, THEN do something with it.
        global state
        state += 1
        
        if state & 1 == 1:        
            self.PinC.toggle()
            self.PinD.toggle()
        else:
            self.PinA.toggle()
            self.PinB.toggle()
        
        # If the motor has completed one full rotation
        if state % 200 == 0:
            state = 0
            self.FullRotation()

    
    # One rotation has been completed
    def FullRotation(self):
        self.RotIndLed.toggle()
    
