from enum import Enum


class CalibrationStatus(Enum):
    Success = 0

    # Please calibrate empty bed first.
    CalibrateEmpty = 1

    # Risk for inaccurate calibration. External vibration detected.
    ExternalVibration = 2

    # Risk for inaccurate calibration. Weak signal detected.
    WeakSignal = 3

    # Risk for inaccurate calibration. External vibration and weak signal detected.
    WeakSignalAndExternalVibration = 7

    # Bed sensor not responding.
    Failed = 8

    # Calibration is in progress.
    InProgress = -1

    # Calibration has not been done after boot.
    NotCalibrated = -2
