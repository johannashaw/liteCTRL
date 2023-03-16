# 
# Pico internet connection protocol 
# February 27, 2023
#
# Sources:
# projects.raspberrypi.org

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

#led = machine.Pin("LED", machine.Pin.OUT)

ssid = "Justin’s iPhone"
password = "deskmate"

# function to connect to WLAN
# Sets up wlan object, activates the wireless,
# and provides ssid and password
def connect():
    #connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # attempt connection until successful
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        pico_led.toggle()
        sleep(1)
        
    # print Pico ip address
    ip = wlan.ifconfig()[0]
    print(f"Connected on: {ip}")
    return ip
    
# A socket is the way a server can listen for a
# client that wants to connect to it.
# In this case, the server is going to be the
# Raspberry Pi Pico W and the client will be a web
# browser on another computer.

# To open a socket, you need to provide the IP address
# and a port number. Port numbers are used by computers
# to identify where requests should be sent.
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def webpage(temperature, state):
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <form action="./lighton">
                <input type="submit" value="Light on"/>
            </form>
            <form action="./lightoff">
                <input type="submit" value="Light off"/>
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
        </body>
        </html>
            '''
    return str(html)

def serve(connection):
    #Start a web server
    state = "OFF"
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        #print(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request == '/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()
        
    

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    print("resetting machine")
    machine.reset()