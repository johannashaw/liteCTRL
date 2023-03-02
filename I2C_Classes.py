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

        # initializes the I2C channels
        self.i2c = I2C(id=0, scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT),  freq=400000)
        # self.i2c = SoftI2C(scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT),  freq=400000)
        
        if 16 not in self.i2c.scan():
            print('VEML7700 is not responding')

        # configure the 7700
        self.I2C_Write(b'00', b'00', b'00')

    
    # Formats the info given so that you can write to the device easily
    def I2C_Write(self, Cmd_code, LSB, MSB):

        buff = 

        # VEML7700 write I2C formatting:
        #   Start condition
        self.i2c.start()
        #   Send Device address
        #   Write bit (0)
        #   ACK
        if self.i2c.write(b'20') != 1:  # address is 16, tehn the write bit
            print("VEML7700:I2C_Write: No ACK was received after address + w was sent")
            self.i2c.stop()
            return 1

        #   Command code
        #   ACK
        if self.i2c.write(Cmd_code) != 1:
            print('VEML7700:I2C_Write: write to command code')
            self.i2c.stop()
            return 2
        
        #   LSB Data
        #   ACK
        if self.i2c.write(LSB) != 1:
            print('VEML7700:I2C_Write: write to command code')
            self.i2c.stop()
            return 3


        #   MSB Data
        #   ACK
        if self.i2c.write(MSB) != 1:
            print('VEML7700:I2C_Write: write to command code')
            self.i2c.stop()
            return 4
        
        #   Stop Condition
        self.i2c.stop()

        return 0

    