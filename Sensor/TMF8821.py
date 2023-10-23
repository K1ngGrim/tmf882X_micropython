from machine import I2C


class TMF8821:
    I2C_ADDRESS = 0x41

    # Sensor register
    ENABLE = 0xE0
    INT_ENAB = 0xE2
    # APPID:Value: If Bootloader is running = 0x03; If application is running = 0x80
    APPID = 0x00
    BOOTLOADER = 0x03
    MEASUREMENT_APP = 0x80
    # First register for Measurement data. 132 bytes following
    DATA_START = 0x24
    STAT_OK = 0x00


    def __init__(self, i2c):
        self.i2c = i2c

    def init_sensor(self):
        I2CHelper.r_write(self.i2c, self.I2C_ADDRESS, self.ENABLE, 0x01)
        data = (0x00).to_bytes(1, 'big')
        while int.from_bytes(data, 'big') != 0x41:
            print('Waiting for Sensor to Enable')
            data = I2CHelper.r_read(self.i2c, self.I2C_ADDRESS, self.ENABLE)

        print('Sensor enabled!')
        app = I2CHelper.r_read(self.i2c, self.I2C_ADDRESS, self.APPID)
        if int.from_bytes(app, 'big') == self.MEASUREMENT_APP:
            print('Measurement application running...')

    def load_factory_calibration(self):
        """
        TODO: not yet fully implemented
        Factory calibration loading means that the host has to do the following steps:
            1. Load the factory calibration page with command LOAD_CONFIG_PAGE_FACTORY_CALIB:
            S 41 W 08 19 P
            2. Check that the command is executed: S 41 W 08 Sr 41 R N P
            This should read back as STAT_OK: 0x00 (if you read back a value >= 0x10 continue to read
            the register 0x08 until it changes to a value less than 0x10)
            3. Check that the configuration page is loaded: S 41 W 20 Sr 41 R A A A N P
            This should read back the values: 0x19 <do not care> 0xBC 0x00
            4. Write the stored calibration data to the I2C registers: 0x24, 0x25, … 0xDF.
            5. Write back the calibration data with command WRITE_CONFIG_PAGE: S 41 W 08 15 P
            6. Check that the command is executed: S 41 W 08 Sr 41 R N P
            This should read back as STAT_OK: 0x00 (if you read back a value >= 0x10 continue to read
            the register 0x08 until it changes to a value less than 0x10)
        """
        I2CHelper.r_write(self.i2c, self.I2C_ADDRESS, 0x08, 0x19)
        data = 0x11
        while data > 0x10:
            print("Waiting for command to be executed...")
            data = int.from_bytes(I2CHelper.r_read(self.i2c, self.I2C_ADDRESS, 0x08))
        print("Command executed")

    def measure_data(self):
        """
        4.3 Measure Command
        After the configuration through the configuration pages and the loading of factory calibration data the
        device is ready for measurements.
            1. Make sure to enable the correct interrupts you want to receive. Enable interrupts for results, set
               the register INT_ENAB to 0x02 if you only want to receive result interrupts, set it to 0x62 if you
               want to receive also error/warning and command done interrupts (see the datasheet for more
               details): S 41 W E2 02 P or S 41 W E2 62 P
            2. Clear any old pending interrupts: S 41 W E1 FF P
            3. The starting of measurements is done by issuing the command MEASURE: S 41 W 08 10 P
            4. The host should check that the command is accepted by reading back the register CMD_STAT:
               S 41 W 08 Sr 41 R N P. This should read back as 0x01 (if a value >= 0x10 is read back then the
               host should continue to read this register, if a value < 0x10 and not 0x01 is returned this is an
               error.)
        """

        I2CHelper.r_write(self.i2c, self.I2C_ADDRESS, self.INT_ENAB, 0x02)
        I2CHelper.r_write(self.i2c, self.I2C_ADDRESS, 0xE1, 0xFF)
        I2CHelper.r_write(self.i2c, self.I2C_ADDRESS, 0x08, 0x10)

        status = 0x11

        timeout = 0
        while status > 0x10:
            print("Waiting for command to be executed... Status: ", status)
            status = int.from_bytes(I2CHelper.r_read(self.i2c, self.I2C_ADDRESS, 0x08), 'big')

            if timeout > 5:
                print("Command timed out")
                return False
            timeout = timeout + 1

        if status != 0x01:
            print("Error occurred!")
            return False

        print("Command executed")


class I2CHelper:

    @staticmethod
    def r_read(i2c: I2C, addr, reg, n_bytes=1):
        """Read byte(s) from specified register. If nbytes > 1, read from consecutive registers."""

        if n_bytes < 1:
            return

        data = i2c.readfrom_mem(addr, reg, n_bytes)

        return data

    @staticmethod
    def r_write(i2c: I2C, addr, reg, data):
        """Write bytes to the specified register."""

        msg = bytearray()
        msg.append(data)

        i2c.writeto_mem(addr, reg, msg)
