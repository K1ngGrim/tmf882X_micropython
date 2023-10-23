from machine import I2C, Pin
from Sensor.TMF8821 import TMF8821

led = Pin(25, Pin.OUT)

i2c = I2C(1, sda=Pin(6), scl=Pin(7))

print('Scan I2C Bus...')
devices = i2c.scan()

# Scanergebnis ausgeben
if len(devices) == 0:
    print('Kein I2C-Gerät gefunden!')
else:
    print('I2C-Geräte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))

sensor = TMF8821(i2c)
sensor.init_sensor()

sensor.measure_data()
