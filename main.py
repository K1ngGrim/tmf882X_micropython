from machine import Pin, I2C, Pin
import TMF8821

led = Pin(25, Pin.OUT)

i2c = I2C(1, sda=Pin(6), scl=Pin(7))

print('Scan I2C Bus...')
devices = i2c.scan()

# # Scanergebnis ausgeben
# if len(devices) == 0:
#     print('Kein I2C-Gerät gefunden!')
# else:
#     print('I2C-Geräte gefunden:', len(devices))
#     for device in devices:
#         print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))


def reg_read(self: I2C, addr, reg, nbytes=1):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """

    # Check to make sure caller is asking for 1 or more bytes
    if nbytes < 1:
        return bytearray()

    # Request data from specified register(s) over I2C
    data = self.readfrom_mem(addr, reg, nbytes)

    return data


def reg_write(self: I2C, addr, reg, data):
    """
    Write bytes to the specified register.
    """

    # Construct message
    msg = bytearray()
    msg.append(data)

    # Write out message to register
    self.writeto_mem(addr, reg, msg)


# Main
reg_write(i2c, 0x41, 0xE0, 0xE0)

while True:
    data = reg_read(i2c, 0x41, 0xE0)
    print('Dezimal Value:', device, '| Hexadezimale Value:', hex(device))
