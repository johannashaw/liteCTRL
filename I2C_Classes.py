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
    #   Light level [lx] is (ALS OUTPUT DATA [dec.] / ALS Gain x responsivity)
    def __init__(self, SCL, SDA):
        # not sure if this is necessary yet but I'm putting it here anyway

        # 000                   -- reserved
        #    00                 -- gain of x1, starting simple
        #      0                -- Res
        #       000             -- Integration time, starting at 100ms (idk)
        #          ??           -- ALS persistence (no idea)
        #            00         -- Res
        #              0        -- Interrupt disabled
        #               0       -- ALS power on

        # initializes the I2C channels
        self.i2c = I2C(id=0, scl=Pin(SCL, mode=Pin.ALT), sda=Pin(SDA, mode=Pin.ALT),  freq=400000)
        
        if 16 not in self.i2c.scan():
            print('VEML7700 is not responding')

    
    # Formats the info given so that you can write to the device easily
    def I2C_Write(self, Cmd_code):

        # VEML7700 write I2C formatting:
        #   Start condition
        self.i2c.start()
        #   Send Device address
        #   Write bit (0)
        self.i2c.write(20)  # address is 16, tehn the write bit
        #   ACK
        #   Command code
        #   ACK
        #   LSB Data
        #   ACK
        #   MSB Data
        #   ACK
        #   Stop Condition

        pass

    