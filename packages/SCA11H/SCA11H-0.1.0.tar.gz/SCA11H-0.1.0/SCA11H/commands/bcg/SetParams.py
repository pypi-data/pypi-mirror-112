from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.bcg.Parameters import Parameters


class SetParams(PostCommand):
    """ Configure BCG Calibration Parameters """

    def __init__(self, params: Parameters, **kwargs):
        super().__init__(endpoint='/bcg/pars', payload='{"pars":"%s"}' % params.to_payload(), **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-bcg-pars'

    @staticmethod
    def get_help():
        return 'Configure BCG Calibration Parameters'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('params',
                            help='BCG calibration parameters as a comma-separated string, e.g.: "7000,270,5000,0,1500,8"')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {'params': Parameters.from_string(args.params)}
