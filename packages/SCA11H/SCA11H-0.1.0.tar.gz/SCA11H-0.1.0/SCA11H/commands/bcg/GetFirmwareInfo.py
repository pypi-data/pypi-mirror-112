from SCA11H.commands.base.GetCommand import GetCommand


class GetFirmwareInfo(GetCommand):
    """ Query BCG Firmware Version """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/bcg/version', **kwargs)

    def run(self, **kwargs) -> str:
        return super().run()['version']

    @staticmethod
    def get_parser_name():
        return 'get-bcg-firmware-info'

    @staticmethod
    def get_help():
        return 'Query BCG Firmware Version'
