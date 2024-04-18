---

# MicroPython TMF882X ToF Sensor Library

## Overview

This project provides a MicroPython library for the TMF882X ToF Sensor family. The TMF8821 is a highly precise Time-of-Flight (ToF) sensor that can be used for various applications. This library facilitates the easy integration of the TMF8821 sensor into MicroPython projects.

## Features

- **Multizone Distance Measurement:** Capture precise distance data with the TMF882X ToF Sensor.

You can find more information about this sensor at [AMS OSRAM](https://ams-osram.com/products/sensors/direct-time-of-flight-sensors-dtof/ams-tmf8821-configurable-4x4-multi-zone-time-of-flight-sensor).

## Installation

1. Ensure you have MicroPython installed on your microcontroller or development board.
2. Copy the project repository into your project.

## Usage

The project does not provide all core functions of this sensor. At the moment, you can initialize the sensor and measure frames.

### Basic Sensor initialization

```python
def func(self):
  self.tof = Tmf8821Utility(ic_com=I2C_com())

  self.tof.log("Try to open connection")
  if Tmf8821App.Status.OK != self.tof.open():
      self.tof.error("Error open FTDI device")
      raise RuntimeError("Error open FTDI device")
  else:
      self.tof.log("Opened connection")

  self.tof.init_bootloader_check()
```

### Measure Frames

```python
def func(self):
  frame = self.tof.measure_frame()

  #do your stuff
```

### Abstractions and Methods

The function of the sensor is abstracted into several classes. `TMF8821_utility` provides simple-to-use methods for the basic functions of this sensor. `TMF8821_app` interfaces with the TMF882X application as a host driver would do. It implements the application's methods as described in the TMF882X datasheet.

## Support

Currently, not all of the sensor's capabilities are implemented in this unofficial library. If you're interested in participating in this project, feel free to contact me. For any questions, issues, or suggestions for improving this project, feel free to create an issue on GitHub.

---

Feel free to customize the content to fit the specific details of your project!
