from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.system.CommunicationSettings import CommunicationSettings


class GetCommunicationSettings(GetCommand):
    """ Query Communication Settings """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/comm', **kwargs)

    def run(self, **kwargs) -> CommunicationSettings:
        return CommunicationSettings.from_payload(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-comm-settings'

    @staticmethod
    def get_help():
        return 'Query Communication Settings'
