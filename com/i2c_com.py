from machine import I2C, Pin


class I2C_Settings:

    def __init__(self, sda: int = 6, scl: int = 7, freq: int = 1000000):
        self.sda_pin = Pin(sda)
        self.scl_pin = Pin(scl)
        self.freq = freq


class I2C_com:

    def __init__(self):
        self.i2c = None

    #
    def i2cOpen(self, i2c_pin_set: I2C_Settings):
        try:
            self.i2c = I2C(1, sda=i2c_pin_set.sda_pin, scl=i2c_pin_set.scl_pin, freq=i2c_pin_set.freq)
            return 0
        except OSError as e:
            return -1

    def i2cTxRx(self, device_addr: int, tx: list, rx_size: int) -> bytearray:
        """Function to transmit and receive bytes via I2C.
        Args:
            device_addr(int): the 7-bit I2C slave address (un-shifted).
            tx(list): the list of bytes to be transmitted.
            rx_size(int): the number of  bytes to be received.
        Returns:
            bytearray: array of bytes received.
        """

        self.i2c.writeto(device_addr, bytes(tx))

        if rx_size == 0:
            return bytearray(0)

        data_buffer = bytearray(rx_size)
        self.i2c.readfrom_into(device_addr, data_buffer)

        return data_buffer

    def i2cTx(self, device_addr: int, tx: list) -> int:
        """Function to transmit given bytes on I2C.
                Args:
                    device_addr(int): the 7-bit I2C slave address (un-shifted).
                    tx(list): a list of bytes to be transmitted.
                Returns:
                    int: status: 0 == ok, else error
                """
        try:
            self.i2c.writeto(device_addr, bytes(tx))
            return 0  # Return 0 indicating success
        except OSError as e:
            print("I2C error:", e)
            return -1  # Indicate an error occurred
