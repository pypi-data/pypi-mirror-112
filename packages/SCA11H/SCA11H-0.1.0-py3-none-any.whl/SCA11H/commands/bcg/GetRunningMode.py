from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.bcg.Mode import Mode
from SCA11H.commands.base import enum_from_value


class GetRunningMode(GetCommand):
    """ Query BCG Running Mode """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg/mode', **kwargs)

    def run(self, **kwargs) -> str:
        return enum_from_value(Mode, int(super().run()['mode']))

    @staticmethod
    def get_parser_name():
        return 'get-bcg-mode'

    @staticmethod
    def get_help():
        return 'Query BCG Running Mode '
