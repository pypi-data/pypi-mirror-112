from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.system.WebpageLanguage import WebpageLanguage
from SCA11H.commands.base import enum_from_value


class SetWebpageLanguage(PostCommand):
    """ Configure Webpage Language """

    def __init__(self, language: WebpageLanguage, **kwargs):
        super().__init__(endpoint='/sys/language', payload='{"language":"%s"}' % language.value, **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-language'

    @staticmethod
    def get_help():
        return 'Configure Webpage Language'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('language', choices=[x.value for x in WebpageLanguage], help='Webpage Language')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {'language': enum_from_value(WebpageLanguage, args.language)}
