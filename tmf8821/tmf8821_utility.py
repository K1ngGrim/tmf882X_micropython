from tmf8821.com.i2c_com import I2C_com, I2C_Settings
from tmf8821.tmf8821_app import Tmf8821App
import time

from tmf8821.tmf8821_device import Tmf8821Device


class Tmf8821Utility(Tmf8821App):

    def __init__(self, ic_com: I2C_com):
        super().__init__(ic_com)

    def open(self, i2c_settings: I2C_Settings = I2C_Settings()):
        return super().open(i2c_settings)

    def init_bootloader_check(self):
        self.enable()

        if not self.isAppRunning():
            self.downloadAndStartApp()
        time.sleep(4)
        print("Application {} started".format(self.getAppId()))

    def measure_frame(self, number_of_frames: int = 1):
        frames = list()
        status = self.startMeasure()
        if status != Tmf8821Device.Status.OK:
            return

        read_frames = 0
        while read_frames < number_of_frames:
            if self.readAndClearInt(self.TMF8X2X_APP_I2C_RESULT_IRQ_MASK):
                read_frames = read_frames + 1
                frame = self.readResult()
                frames.append(frame)
                break

        self.stopMeasure()
        return frames
