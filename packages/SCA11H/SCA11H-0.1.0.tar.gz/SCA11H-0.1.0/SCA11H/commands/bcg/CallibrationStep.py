class CalibrationStep:
    def __init__(self, step: int):
        self.step = step

    def __str__(self):
        if self.step == 0:
            return 'CalibrationStart'
        elif self.step == 255:
            return 'CalibrationEnd'
        else:
            return '%.2f%%' % (100.0 / 60.0 * self.step)
