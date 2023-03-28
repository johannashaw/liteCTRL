from machine import Pin, Timer

# maps to pico pin 34
# also ground is pin 38, I think. I'm not sure 
led = machine.Pin(28, Pin.OUT)
tim = Timer()
def tick(timer):
    led.toggle()
tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)