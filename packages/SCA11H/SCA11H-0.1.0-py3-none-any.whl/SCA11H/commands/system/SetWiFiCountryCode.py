from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.system.WiFiCountryCode import WiFiCountryCode
from SCA11H.commands.base import enum_from_value


class SetWiFiCountryCode(PostCommand):
    """ Configure WiFi Country Code """

    def __init__(self, country: WiFiCountryCode, **kwargs):
        super().__init__(endpoint='/sys/country', payload='{"country":"%s"}' % country.value, **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-country'

    @staticmethod
    def get_help():
        return 'Configure WiFi Country Code'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('country', choices=[x.value for x in WiFiCountryCode], help='WiFi Country Code')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {'country': enum_from_value(WiFiCountryCode, args.country)}
