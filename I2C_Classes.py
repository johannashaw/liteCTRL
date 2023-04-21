# Project: liteCTRL
# File: Custom I2C classes. Contains class defs for the following:
#           - VEML7700 (ambient light sensor)
#           - APDS9960 (light and light temp sensor)
#           - LED_Strip (maybe, depends if it needs I2C)
# Created by: Johanna Shaw
from machine import Pin, I2C, SoftI2C
# from LEDStrip import Colour

# Base class for both sensors. 
# Created under the assumption that both sensors are using the same I2C channel and this class ensures that they are.
class base_i2c:
    i2c = None

    def __init__(self, SCL, SDA):
        # Sets the I2C channel at a class level
        #uses SoftI2C to allow more control over the channel
        base_i2c.i2c = SoftI2C(scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT), freq=400000, timeout=35000)


# the ambient light sensor
class VEML7700(base_i2c):
    # Attributes:
    address = 0x10    # PLEASE DON'T CHANGE THIS, address = 16
    
    # Note:
    #   ALS means Ambient Light Sensor
    #   Light level [lx] is (ALS OUTPUT DATA [dec.] / ALS Gain x responsivity)
    def __init__(self):
        # I2C channel needs to be initialized.
        if base_i2c.i2c is None:
            raise Exception('You forgot to initialize the base I2C channel')

        # Checks if the device is responding to calls
        if self.address not in base_i2c.i2c.scan():
            raise Exception('VEML7700 is not responding')
        else:
            print('VEML7700 says hi')

        # 000                       -- reserved
        #    0 0                    -- gain of x1, starting simple
        #       0                   -- Res
        #        00 00              -- Integration time, starting at 100ms (idk)
        #             ??            -- ALS persistence (no idea)
        #                00         -- Res
        #                  0        -- Interrupt disabled
        #                   0       -- ALS power on
        # 0000 0000 1000 0000   MSB = 0C, LSB = 00
        # MSB       LSB

        # configure the 7700
        if  self.Write(Cmd_code=0x00, MSB= 0x00, LSB=0x00) != 0:            
            raise Exception('VEML7700 failed to initialize')

    
    # Formats the info given so that you can write to the device easily
    def Write(self, Cmd_code, LSB, MSB):
        # buff = Cmd_code + LSB + MSB
        buff = bytes([self.address << 1] + [Cmd_code] + [LSB] + [MSB])

        # VEML7700 write I2C formatting:
        #   Start condition
        base_i2c.i2c.start()
        #   Send Device address
        #   Write bit (0)
        #   ACK
        #   Command code
        #   ACK        
        #   LSB Data
        #   ACK
        #   MSB Data
        #   ACK        

        # temp = self.i2c.writeto(16, buff, True)
        temp = base_i2c.i2c.write(buff)

        if temp != 4:
            print(f'VLEM7700:Write: 4 ACK expected, {temp} ACK received')
            return 1

        #   Stop Condition
        base_i2c.i2c.stop()

        return 0
    
    
    def Read(self, Cmd_code, ):

        buff = bytes([self.address << 1] + [Cmd_code])
        
        # start
        base_i2c.i2c.start()
        # device address
        # write bit
        # ACK
        # Command code      ##
        # ACK

        temp = base_i2c.i2c.write(buff)
        if temp != 2:
            print(f'VLEM7700:Read: Write command: 2 ACK expected, {temp} ACK received')
            return None#1
        
        buff = bytes([(self.address << 1) + 1] )

        # Start
        base_i2c.i2c.start()
        # device address
        # read bit
        # ACK

        temp = base_i2c.i2c.write(buff)
        if temp != 1:
            print(f'VLEM7700:Read: Read command: 1 ACK expected, {temp} ACK received')
            return None #2
        
        read = bytearray(2)        

        ## receive LSB      ##
        # we ACK

        # receive MSB
        # we don't ACK      ##        
        base_i2c.i2c.readinto(read,True)

        # Stop bit
        base_i2c.i2c.stop()       

        # return formatted(?) data

        return int.from_bytes(read, "little")      # assuming that the readinto method stores starting at 0
    
        # return int.from_bytes(read, "big")        # if readinto starts in reverse order for some reasom

    
    # Returns the ALS High Res Output Data
    # Lux = ALS_output / (Gain * integration_time[ms] / 10)
    def Get_Lux(self):
        # Uses Command code #4 ( 04h, idk)
        # if you're using a different integration time you'll need to change this.
        return self.Read(4) / 10
    

    # Returns the white value (?)
    def Get_White(self):
        return self.Read(5)


# NOTE: READ AND WRITE AREN'T TESTED
class APDS9960(base_i2c):
    address = 0x39

    def __init__(self):
        # the cannel needs to be initialized in order for the sensor to be used
        if base_i2c.i2c is None:
            raise Exception('You forgot to initialize the base I2C channel')

        # Checks if the device is responding to calls
        if self.address not in base_i2c.i2c.scan():
            raise Exception('APDS9960 is not responding')
        else:
            print('APDS9960 says hi')

        # Remember that you need to actually initialize the bloody device
        # bit 0 = power on
        # bit 1 = ALS Enable
        if self.Write(0x80, 0x03) != 0:
            raise Exception('APDS9960 not initialized')
        # set integration time to 100ms
        self.Write(0x81, 220)

        # Control Reg 1 (set gain)
        self.Write(0x8F, 0x00)


    def Write(self, Reg, Data):

        buff = bytes([self.address << 1] + [Reg] + [Data])

        # Start
        base_i2c.i2c.start()
        # Address [7]
        # Write = 0 [1]
        # ACK
        # Register_Address [8]
        # ACK
        # Data [8]
        # ACK

        temp = base_i2c.i2c.write(buff)
        if temp != 3:
            print(f'APDS9960:Write: 3 ACK expected, {temp} ACK received')
            return 1

        # Stop
        base_i2c.i2c.stop()

        return 0

    def Read(self, Reg, numbytes):
        buff = bytes([self.address << 1] + [Reg])

        # Start
        base_i2c.i2c.start()
        # Address [7]
        # Write = 0 [1]
        # ACK
        # Register_Address [8]
        # ACK

        temp = base_i2c.i2c.write(buff)
        if temp != 2:
            print(f'VLEM7700:Read: Write command ({Reg:X}): 2 ACK expected, {temp} ACK received')
            return None#1

        buff = bytes([(self.address << 1) + 1])
        # Start
        base_i2c.i2c.start()
        # Address [7]
        # Read = 1 [1]
        # ACK
        
        temp = base_i2c.i2c.write(buff)
        if temp != 1:
            print(f'VLEM7700:Read: Read command ({Reg:X}): 1 ACK expected, {temp} ACK received')
            return None#1

        read = bytearray(numbytes)
        # Data [8]
        # ACK (us)
        # Data [8]
        # ACK (us)
        base_i2c.i2c.readinto(read, True)

        # stop
        base_i2c.i2c.stop()

        return read


    def GetCRGB(self):
        # Get the Clear + RGB values
        CRGB =self.Read(0x94, 8)        # read 8 bytes starting at reg 0x94 (clear lower to blue high)

        # Clear value can translate to ambient light
        clear = int.from_bytes(CRGB[0:2], "little")     # this subarray but here is first number inclusive, second exclusive

        # get red
        red = int.from_bytes(CRGB[2:4], "little")
         

        # get Green
        green = int.from_bytes(CRGB[4:6], "little")


        # get Blue
        blue = int.from_bytes(CRGB[6:8], "little")

        
        lux = int((clear + 288) / 1.64)

        # stop bit        
        # base_i2c.i2c.stop()

        # print (f"CRGB = {CRGB}")#, green = {green}, blue = {blue}")
        # print(f'clear ={clear}, red = {red}, green = {green}, blue = {blue}')

        # Return RGB
        return lux, clear, red, green, blue

