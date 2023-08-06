from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.bcg.CalibrationPhase import CalibrationPhase
from SCA11H.commands.bcg.CalibrationStatus import CalibrationStatus
from SCA11H.commands.bcg.CallibrationStep import CalibrationStep
from SCA11H.commands.base import enum_from_value
from typing import Dict


class CalibrationInfo:
    def __init__(self, payload: Dict[str, str]):
        self.status = enum_from_value(CalibrationStatus, payload['status'])

        if 'phase' in payload:
            self.phase = enum_from_value(CalibrationPhase, payload['phase'])
        else:
            self.phase = None

        if 'step' in payload:
            self.step = CalibrationStep(step=int(payload['step']))
        else:
            self.step = None

    def __str__(self):
        return '\n'.join(self.as_list())

    def as_list(self):
        return [
            'Status: %s' % self.status,
            'Phase:  %s' % self.phase,
            'Step:   %s' % self.step
        ]


class GetCalibrationStatus(GetCommand):
    """ Query BCG Calibration Status """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg/cali', **kwargs)

    def run(self, **kwargs) -> CalibrationInfo:
        return CalibrationInfo(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-bcg-calibration'

    @staticmethod
    def get_help():
        return 'Query BCG Calibration Status'
