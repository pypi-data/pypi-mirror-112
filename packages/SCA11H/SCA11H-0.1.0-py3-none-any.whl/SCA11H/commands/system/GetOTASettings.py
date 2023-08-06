from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.system.OTASettings import OTASettings


class GetOTASettings(GetCommand):
    """ Query OTA Settings """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/ota', **kwargs)

    def run(self, **kwargs) -> OTASettings:
        return OTASettings.from_payload(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-ota-settings'

    @staticmethod
    def get_help():
        return 'Query OTA Settings'
