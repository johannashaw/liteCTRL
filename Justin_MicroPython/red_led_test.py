from machine import Pin, Timer
red_led = machine.Pin(15, Pin.OUT)
blue_led = machine.Pin(14, Pin.OUT)
green_led = machine.Pin(13, Pin.OUT)
yellow_led = machine.Pin(12, Pin.OUT)

red_led.on()
green_led.on()

tim = Timer()

def tick(timer):
    red_led.toggle()
    blue_led.toggle()
    green_led.toggle()
    yellow_led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
