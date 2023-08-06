from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.base import enum_from_value
from SCA11H.commands.system.WebpageLanguage import WebpageLanguage


class GetWebpageLanguage(GetCommand):
    """ Query Webpage Language """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/language', **kwargs)

    def run(self, **kwargs) -> WebpageLanguage:
        return enum_from_value(WebpageLanguage, super().run()['language'])

    @staticmethod
    def get_parser_name():
        return 'get-language'

    @staticmethod
    def get_help():
        return 'Query Webpage Language'
