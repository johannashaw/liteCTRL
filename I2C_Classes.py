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
        self.i2c = I2C(id=0, scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT),  freq=400000)
        # self.i2c = SoftI2C(scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT),  freq=400000)
        
        if 16 not in self.i2c.scan():
            print('VEML7700 is not responding')

        # configure the 7700
        #self.I2C_Write(b'00', MSB=b'0C', LSB=b'00')
        self.i2c.writeto_mem(16, 4, b'0000', addrsize=16)

    
    # Formats the info given so that you can write to the device easily
    def I2C_Write(self, Cmd_code, LSB, MSB):

        buff = Cmd_code + LSB + MSB

        # VEML7700 write I2C formatting:
        #   Start condition
        #   Send Device address
        #   Write bit (0)
        #   ACK
        #   Command code
        #   ACK        
        #   LSB Data
        #   ACK
        #   MSB Data
        #   ACK        
        #   Stop Condition

        temp = self.i2c.writeto(16, buff, True)
        if temp != 4:
            print(f'VLEM7700:I2C_Write: 4 ACK expected, {temp} ACK received')
            return 1

        return 0
    
    def I2C_Read(self, Cmd_code):
        
        # start
        # device address
        # write bit
        # ACK
        # Command code      ##
        # ACK
        temp = self.i2c.writeto(16, Cmd_code, False)
        if temp != 2:
            print(f'VLEM7700:I2C_Read: 4 ACK expected, {temp} ACK received')
            return 1

        # Start
        # device address
        # read bit
        # ACK
        ## receive LSB      ##
        # we ACK
        # receive MSB
        # we don't ACK      ##
        # Stop bit

        # I2C.readfrom(addr, nbytes, stop=True, /)
        byRead  = self.i2c.readfrom(16, 2, True)
        

        # return LSB and MSB
        #print(byRead)

        return byRead

    
    # Returns the ALS High Res Output Data
    def Get_Lux(self):
        # Uses Command code #4 ( 04h, idk)
        # return self.I2C_Read(b'04')
        return I2C.readfrom_mem(16, 4, 2, addrsize=16)


    