from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.base import enum_from_value
from SCA11H.commands.system.WiFiCountryCode import WiFiCountryCode


class GetWiFiCountryCode(GetCommand):
    """ Query WiFi Country Code """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/country', **kwargs)

    def run(self, **kwargs) -> WiFiCountryCode:
        return enum_from_value(WiFiCountryCode, super().run()['country'])

    @staticmethod
    def get_parser_name():
        return 'get-country'

    @staticmethod
    def get_help():
        return 'Query WiFi Country Code'
