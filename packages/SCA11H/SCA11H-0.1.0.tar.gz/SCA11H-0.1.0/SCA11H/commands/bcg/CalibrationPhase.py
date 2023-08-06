from enum import Enum


class CalibrationPhase(Enum):
    # Empty bed calibration.
    EmptyBed = 1

    # Occupied bed calibration
    OccupiedBed = 2
