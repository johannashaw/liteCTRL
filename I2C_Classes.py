# Project: liteCTRL
# File: Custom I2C classes. Contains class defs for the following:
#           - VEML7700 (ambient light sensor)
#           - APDS9960 (light and light temp sensor)
#           - LED_Strip (maybe, depends if it needs I2C)
# Created by: Johanna Shaw
from machine import Pin, I2C, SoftI2C


# the ambient light sensor
class VEML7700:
    # Attributes:
    address = 16    # PLEASE DON"T CHANGE THIS
    
    # Note:
    #   ALS means Ambient Light Sensor
    #   Light level [lx] is (ALS OUTPUT DATA [dec.] / ALS Gain x responsivity)
    def __init__(self, SCL, SDA):
        # not sure if this is necessary yet but I'm putting it here anyway

        # 000                   -- reserved
        #    00                 -- gain of x1, starting simple
        #      0                -- Res
        #       0000            -- Integration time, starting at 100ms (idk)
        #           ??          -- ALS persistence (no idea)
        #             00        -- Res
        #               0       -- Interrupt disabled
        #                0      -- ALS power on
        # 0000 1100 0000 0000   MSB = 0C, LSB = 00

        # initializes the I2C channels
        # self.i2c = I2C(id=0, scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT),  freq=400000)
        self.i2c = SoftI2C(scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT), freq=400000, timeout=35000)

        
        if 16 not in self.i2c.scan():
            print('VEML7700 is not responding')
        else:
            print('VEML7700 says hi')

        # configure the 7700
        # self.I2C_Write(b'\x00', MSB=b'\x0C', LSB=b'\x00')
        self.I2C_Write(0, MSB= 12, LSB=0)

    
    # Formats the info given so that you can write to the device easily
    def I2C_Write(self, Cmd_code, LSB, MSB):
        # buff = Cmd_code + LSB + MSB
        buff = bytes([self.address << 1] + [Cmd_code] + [LSB] + [MSB])

        # VEML7700 write I2C formatting:
        #   Start condition
        self.i2c.start()
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
        temp = self.i2c.write(buff)

        if temp != 4:
            print(f'VLEM7700:I2C_Write: 4 ACK expected, {temp} ACK received')
            return 1

        #   Stop Condition
        self.i2c.stop()

        return 0
    
    
    def I2C_Read(self, Cmd_code):

        buff = bytes([self.address << 1] + [Cmd_code])
        
        # start
        self.i2c.start()
        # device address
        # write bit
        # ACK
        # Command code      ##
        # ACK

        # temp = self.i2c.writeto(16, Cmd_code, False)
        temp = self.i2c.write(buff)
        if temp != 2:
            print(f'VLEM7700:I2C_Read: Write command: 2 ACK expected, {temp} ACK received')
            return 1
        
        buff = bytes([(self.address << 1) + 1] + [Cmd_code])

        # Start
        self.i2c.start()
        # device address
        # read bit
        # ACK

        temp = self.i2c.write(buff)
        if temp != 1:
            print(f'VLEM7700:I2C_Read: Read command: 1 ACK expected, {temp} ACK received')
            return 2
        
        read = bytearray(2)        

        ## receive LSB      ##
        # we ACK

        # receive MSB
        # we don't ACK      ##        
        self.i2c.readinto(read, True)

        # Stop bit
        self.i2c.stop()

        # I2C.readfrom(addr, nbytes, stop=True, /)
        # byRead  = self.i2c.readfrom(16, 2, True)
        

        # return LSB and MSB
        # byRead = (int.from_bytes(MSB, "big") << 8) + int.from_bytes(LSB, "big")
        # print(byRead)
        # print(MSB)
        print(read)

        print(int.from_bytes(read, "big"))
        print(int.from_bytes(read, "little"))

        # assuming 

        # print(int.from_bytes(MSB, "big"))

        # return (int.from_bytes(MSB, "big") << 8) + int.from_bytes(LSB, "big")

        return int.from_bytes(read, "little")      # assuming that the readinto method stores starting at 0

    
    # Returns the ALS High Res Output Data
    def Get_Lux(self):
        # Uses Command code #4 ( 04h, idk)
        # return self.I2C_Read(b'04')
        return self.I2C_Read(4)


