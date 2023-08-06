from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.bcg.Mode import Mode
from SCA11H.commands.bcg.Direction import Direction
from SCA11H.commands.bcg.Parameters import Parameters
from SCA11H.commands.base import enum_from_value
from typing import Dict


class BCGInfo:
    def __init__(self, payload: Dict[str, str]):
        self.version = payload['version']
        self.mode = enum_from_value(Mode, int(payload['mode']))
        self.pars = Parameters.from_string(payload['pars'])
        self.dir = enum_from_value(Direction, payload['dir'])

    def as_list(self):
        lines = ['   %s' % x for x in self.pars.as_list()]

        res = [
            'Version:    %s' % self.version,
            'Mode:       %s' % self.mode.name,
            'Direction:  %s' % self.dir.name,
            'Parameters:\n%s' % '\n'.join(lines),
        ]
        return res

    def __str__(self):
        return '\n'.join(self.as_list())


class GetBasicInfo(GetCommand):
    """ Query Basic BCG Info """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg', **kwargs)

    def run(self, **kwargs) -> BCGInfo:
        return BCGInfo(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-bcg-info'

    @staticmethod
    def get_help():
        return 'Query Basic BCG Info'
