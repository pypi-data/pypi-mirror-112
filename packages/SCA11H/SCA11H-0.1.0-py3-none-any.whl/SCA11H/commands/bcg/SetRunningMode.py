from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.bcg.Mode import Mode
from SCA11H.commands.base import enum_from_value


class SetMode(PostCommand):
    """ Configure BCG Running Mode """

    def __init__(self, mode: Mode, **kwargs):
        super().__init__(endpoint='/bcg/mode', payload='{"mode":%d}' % mode.value, **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-bcg-mode'

    @staticmethod
    def get_help():
        return 'Configure BCG Running Mode'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('mode', choices=[str(x.value) for x in Mode],
                            help='BCG Mode; 0 - BCG (The module measures acceleration with 1kHz interval and runs the '
                                 'result through the algorithm. Processed output data is sent at 1Hz rate); 1 - '
                                 'DataLogger (1-axis, AC. The module measures and sends raw acceleration data with '
                                 '1kHz)')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {'mode': enum_from_value(Mode, int(args.mode))}
