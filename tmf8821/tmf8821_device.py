import time
from com.i2c_com import I2c_com


class Tmf8821Device:
    class Status:
        """The status return code of a method. either OK (=0), or an error (<>0)"""
        OK = 0
        """The function executed as expected."""
        DEV_ERROR = -1
        """The TMF882X device had a protocol error (e.g. the device FLASH reported an error over I2C)."""
        APP_ERROR = -2
        """The TMF882X device application had a protocol error (e.g. the device firmware reported an error over I2C)."""
        TIMEOUT_ERROR = -3
        """The TMF882X device did not respond in time (e.g. found no SPI device)."""
        UART_ERROR = -4
        """Something went wrong when opening or reading from UART."""
        OTHER_ERROR = -5
        """Something went wrong, but there's no specific error code."""

    I2C_SLAVE_ADDR = 0x41
    """The default I2C address. Fixed for now, can be changed later. """

    class ExceptionLevel:
        """The exception level that defines until where an error shall throw an exception. """
        OFF = 0
        """Do not throw exceptions."""
        FTDI = 1
        """Throw exceptions on FTDI level (e.g., I2C-TX failed)"""
        DEVICE = 2
        """Throw exceptions on device level (e.g., could not enable device, SPI device not found, UART RX timed out)"""
        APP = 3
        """Throw exceptions on application level (e.g., command timed out, application reported error)"""

    TMF882X_ENABLE = 0xe0
    TMF882X_ENABLE__ready__MASK = 1 << 6
    TMF882X_ENABLE__wakeup__MASK = 1 << 0
    TMF882X_WAKEUP = TMF882X_ENABLE__ready__MASK | TMF882X_ENABLE__wakeup__MASK

    TMF882X_INT_STATUS = 0xe1
    TMF882X_INT_ENAB = 0xe2

    def __init__(self, com: I2c_com):
        self.com = com
        self.register_buffer = [0xff] * 256
        self.power_up_mask = 0x41

    def open(self, i2c_speed: int = 1000000):
        """
        Open the communication.
        Args:
            i2c_speed (int, optional): Open I2C communication. Defaults to 1000000.
        Returns:
            Status: The status code (OK = 0, error != 0)..
        """
        return self.com.i2cOpen(i2c_speed=i2c_speed)

    def enable(self, send_wake_up_sequence: bool = True) -> int:
        """Enable the TMF882X.
        Args:
            send_wake_up_sequence (bool, optional): Send the I2C power-on sequence from a cold start. Defaults to True.
        Returns:
            Status: The status code (OK = 0, error != 0)..
        """

        if send_wake_up_sequence:
            time.sleep(0.010)
            # Initial wakeup is simpler
            return self.powerUp()
        return self.Status.OK

    def powerUp(self) -> int:
        self.power_up_mask = self.com.i2cTxRx(self.I2C_SLAVE_ADDR, [self.TMF882X_ENABLE], 1)[0]
        self.power_up_mask = self.power_up_mask | self.TMF882X_ENABLE__wakeup__MASK
        self.com.i2cTx(self.I2C_SLAVE_ADDR, [self.TMF882X_ENABLE, self.power_up_mask])  # request a power up = wakeup
        time.sleep(0.010)
        enable = self.com.i2cTxRx(self.I2C_SLAVE_ADDR, [self.TMF882X_ENABLE], 1)
        enable = self.com.i2cTxRx(self.I2C_SLAVE_ADDR, [self.TMF882X_ENABLE],
                                  1)  # need to read twice to have HW change the return the correct value
        if len(enable) < 1 or enable[0] & self.TMF882X_ENABLE__ready__MASK != self.TMF882X_ENABLE__ready__MASK:
            print("The device didn't power up as expected (ENABLE register value is: ", enable, "). please check you "
                                                                                                "hardware setup.")
            return self.Status.DEV_ERROR
        self.com.i2cTx(self.I2C_SLAVE_ADDR, [self.TMF882X_ENABLE, enable[0] | self.TMF882X_ENABLE__wakeup__MASK])
        return self.Status.OK

    def _setError(self, message):
        """An error occurred - add it to the error list, which the host can later read out.

        Args:
            message (str): The errorr message
        """
        print(message)

    def _log(self, message):
        """Log information"""
        print(message)

    def readIntStatus(self) -> int:
        """ read the interrupt status register of TMF8x0x """
        intreg = self.com.i2cTxRx(self.I2C_SLAVE_ADDR, [self.TMF882X_INT_STATUS], 1)
        if len(intreg):
            return intreg[0]
        self._setError("Cannot read the INT_STATUS register")
        return 0

    def clearIntStatus(self, bitMaskToClear):
        """ clear the interrupt status register of TMF8x0x
         Args:
            bitMaskToClear: all bits set in this 8-bit mask will be cleared in the interrupt register
        """
        self.com.i2cTx(self.I2C_SLAVE_ADDR, [self.TMF882X_INT_STATUS, bitMaskToClear])

    def readIntEnable(self) -> int:
        """ read the interrupt enable register of TMF8x0x """
        enabreg = self.com.i2cTxRx(self.I2C_SLAVE_ADDR, [self.TMF882X_INT_ENAB], 1)
        if len(enabreg):
            return enabreg[0]
        self._setError("Cannot read the INT_STATUS register")
        return 0

    def enableInt(self, bitMaskToEnable):
        """ enable all the interrupts that have the bit set in the parameter, all other interrupts will be disabled
         Args:
            bitMaskToEnable: all bits set in this 8-bit mask will be enabled, all others disabled
        """
        self.com.i2cTx(self.I2C_SLAVE_ADDR, [self.TMF882X_INT_ENAB, bitMaskToEnable])

    def clearAndEnableInt(self, bitMaskToEnable):
        """
        Clear and enable given interrupt bits
        Args:
            bitMaskToEnable : all bits set in this 8-bit mask will be cleared and enabled, all others disabled
        """
        self.clearIntStatus(bitMaskToEnable)  # first clear any old pending interrupt
        self.enableInt(bitMaskToEnable)  # now clear it

    def readAndClearInt(self, bitMaskToCheck):
        """
        Check if given interrupt bits are set, if they are, clear them and return them
        Args:
            bitMaskToCheck (TYPE): bit mask for interrupts to check for
        Returns:
            clr (TYPE): set interrupt bits that also have been cleared
        """
        clr = self.readIntStatus() & bitMaskToCheck
        if clr:
            self.clearIntStatus(clr)
        return clr
