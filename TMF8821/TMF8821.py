from machine import I2C

class TMF8821:
    ADDRESS = 0x41

    def __init__(self, i2c):
        self.i2c = i2c
