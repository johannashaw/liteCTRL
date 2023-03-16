from machine import Pin, Timer
from time import sleep


# Output pin assignment
A = machine.Pin(15, Pin.OUT)
NOT_A = machine.Pin(14, Pin.OUT)
B = machine.Pin(13, Pin.OUT)
NOT_B = machine.Pin(12, Pin.OUT)

# Begin in step ONE
A.on()
NOT_A.off()
B.on()
NOT_B.off()


tim = Timer()

def tick(timer):
    
    # sleep(5)
    
    if A.value() and NOT_B.value(): # Step ONE
        NOT_B.off()
        B.on()
    elif A.value() and B.value(): # Step TWO
        A.off()
        NOT_A.on()
    elif NOT_A.value() and B.value(): # Step THREE
        B.off()
        NOT_B.on()
    elif NOT_A.value() and NOT_B.value(): # Step FOUR
        A.on()
        NOT_A.off()
        
    

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)


