from enum import Enum


class Mode(Enum):
    # The module measures acceleration with 1kHz interval and runs the result through the algorithm. Processed output
    # data is sent at 1Hz rate
    BCG = 0

    # 1 - axis, AC.The module measures and sends raw acceleration data with 1kHz
    DataLogger = 1
