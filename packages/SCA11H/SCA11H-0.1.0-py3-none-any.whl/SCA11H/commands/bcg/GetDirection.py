from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.bcg.Direction import Direction
from SCA11H.commands.base import enum_from_value


class GetDirection(GetCommand):
    """ Query BCG Measurement Direction """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg/dir', **kwargs)

    def run(self, **kwargs) -> str:
        return enum_from_value(Direction, int(super().run()['dir']))

    @staticmethod
    def get_parser_name():
        return 'get-bcg-dir'

    @staticmethod
    def get_help():
        return 'Query BCG Measurement Direction'
