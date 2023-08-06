from enum import Enum
from time import sleep

from SCA11H.commands.bcg.CalibrationPhase import CalibrationPhase
from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.base import enum_from_value
from SCA11H.commands.bcg.CalibrationStatus import CalibrationStatus
from SCA11H.commands.bcg.GetCalibrationStatus import CalibrationInfo


class StartResult(Enum):
    # BCG calibration started successfully
    Started = 0

    # BCG calibration start failed
    StartFailed = -1

    # Calibration is in progress
    InProgress = -2

    # Calibration is disabled in cloud mode because URL is blank
    Unsupported = -3

    # Shouldn't be received from BCN, used internally as result
    CalibrationFinished = 1


def default_callback(status: CalibrationInfo):
    if status.status == CalibrationStatus.InProgress:
        print('-' * 10)
        print(status)
        sleep(5)


class StartCalibration(PostCommand):
    """ Start BCG Calibration """

    def __init__(self, phase: CalibrationPhase, wait_for_completion: bool, progress_callback=default_callback,
                 **kwargs):
        super().__init__(endpoint='/bcg/cali', payload='{"phase":%d}' % phase.value, **kwargs)
        self.kwargs = kwargs
        self.wait_for_completion = wait_for_completion
        self.progress_callback = progress_callback

    def run(self, **kwargs) -> StartResult:
        post_result = super().run(checked=False, **kwargs)
        res = enum_from_value(StartResult, post_result.errno)
        if (res != StartResult.Started and res != StartResult.InProgress) or not self.wait_for_completion:
            return res

        sleep(2)

        from SCA11H.commands.bcg.GetCalibrationStatus import GetCalibrationStatus
        for i in range(65):
            status = GetCalibrationStatus(**self.kwargs).run()
            if status.status == CalibrationStatus.InProgress:
                self.progress_callback(status)
            elif status.status == CalibrationStatus.Success:
                return StartResult.CalibrationFinished
            else:
                raise Exception(status.status.name)

        return StartResult.InProgress

    @staticmethod
    def get_parser_name():
        return 'start-bcg-calibration'

    @staticmethod
    def get_help():
        return 'Start BCG Calibration'

    @staticmethod
    def add_arguments(parser):
        phase = parser.add_mutually_exclusive_group()
        phase.add_argument('--empty', '-e', action='store_true', help='Empty bed calibration')
        phase.add_argument('--occupied', '-o', action='store_true', help='Occupied bed calibration')
        parser.add_argument('--wait', '-w', action='store_true', help='Wait for calibration completion')

    @staticmethod
    def parse_arguments(args) -> dict:
        if args.empty:
            phase = CalibrationPhase.EmptyBed
        elif args.occupied:
            phase = CalibrationPhase.OccupiedBed
        else:
            raise Exception('Phase value expected')

        return {'phase': phase, 'wait_for_completion': args.wait}
