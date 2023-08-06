from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.bcg.Parameters import Parameters


class GetParams(GetCommand):
    """ Query BCG Calibration Parameters """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg/pars', **kwargs)

    def run(self, **kwargs) -> Parameters:
        return Parameters.from_string(super().run()['pars'])

    @staticmethod
    def get_parser_name():
        return 'get-bcg-pars'

    @staticmethod
    def get_help():
        return 'Query BCG Calibration Parameters'
