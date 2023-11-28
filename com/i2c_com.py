from machine import I2C, Pin


class I2c_com:

    def __init__(self):
        self.i2c = None

    def i2cOpen(self, i2c_speed: int):
        try:
            self.i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=i2c_speed)
            return 0
        except OSError as e:
            return -1

    def i2cTxRx(self, devaddr: int, tx: list, rx_size: int) -> bytearray:
        """Function to transmit and receive bytes via I2C.
        Args:
            devaddr(int): the 7-bit I2C slave address (un-shifted).
            tx(list): the list of bytes to be transmitted.
            rx_size(int): the number of  bytes to be received.
        Returns:
            bytearray: array of bytes received.
        """

        self.i2c.writeto(devaddr, bytes(tx))

        if rx_size == 0:
            return bytearray(0)

        data_buffer = bytearray(rx_size)
        self.i2c.readfrom_into(devaddr, data_buffer)

        return data_buffer

    def i2cTx(self, devaddr: int, tx: list) -> int:
        """Function to transmit given bytes on I2C.
                Args:
                    devaddr(int): the 7-bit I2C slave address (un-shifted).
                    tx(list): a list of bytes to be transmitted.
                Returns:
                    int: status: 0 == ok, else error
                """
        try:
            self.i2c.writeto(devaddr, bytes(tx))
            return 0  # Return 0 indicating success
        except OSError as e:
            print("I2C error:", e)
            return -1  # Indicate an error occurred
