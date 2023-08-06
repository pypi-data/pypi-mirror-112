from SCA11H.commands.base.GetCommand import GetCommand


class GetSerial(GetCommand):
    """ Query BCG Serial Number """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg/sn', **kwargs)

    def run(self, **kwargs) -> str:
        return super().run()['sn']

    @staticmethod
    def get_parser_name():
        return 'get-bcg-serial'

    @staticmethod
    def get_help():
        return 'Query BCG Serial Number'
