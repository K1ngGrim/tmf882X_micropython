import time

from com.i2c_com import I2c_com
from tmf8821.tmf8821_app import Tmf8821App


def measure(tof: Tmf8821App, number_of_frames: int, log: bool = False):
    """
    Start a measurement and read number_of_frames, then stop the measurement

    Args:
        tof (Tmf882xApp): the tof instance.
        log (bool, optional): DESCRIPTION. Defaults to False.
        number_of_frames (int): the number of frames to measure. Defaults to 100
        log (bool, optional): Whether to print to console or not. Defaults to False.
    """
    tof.startMeasure()
    read_frames = 0
    while read_frames < number_of_frames:
        if tof.readAndClearInt(tof.TMF8X2X_APP_I2C_RESULT_IRQ_MASK):
            read_frames = read_frames + 1
            frame = tof.readResult()

            data_list, _ = tof.getResultFields(frame)
            row = ["#obj"] + data_list
            if log:
                print("Frame[{}]:".format(read_frames), row)  # regular result frame header
    tof.stopMeasure()


def execute(tof: Tmf8821App):
    tof.enable()
    tof.downloadAndStartApp()

    time.sleep(0.5)  # give the application some time to fully start up.
    print("Application {} started".format(tof.getAppId()))

    tof.configure(period_in_ms=33, kilo_iterations=537,
                  spad_map_id=Tmf8821App.TMF8X2X_COM_SPAD_MAP_ID__spad_map_id__map_no_7)
    measure(tof, number_of_frames=30, log=True)


if __name__ == "__main__":
    com = I2c_com()

    tof = Tmf8821App(ic_com=com)

    if Tmf8821App.Status.OK != tof.open(i2c_speed=400000):  # open FTDI communication channels
        raise RuntimeError("Error open FTDI device")

    execute(tof)
