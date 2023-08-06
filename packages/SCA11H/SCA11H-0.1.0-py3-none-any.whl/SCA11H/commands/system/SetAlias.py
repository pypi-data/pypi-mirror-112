from SCA11H.commands.base.PostCommand import PostCommand


class SetAlias(PostCommand):
    """ Configure BSN Name """

    def __init__(self, name: str, **kwargs):
        super().__init__(endpoint='/sys', payload='{"alias":"%s"}' % name, **kwargs)
        if len(name.encode('ascii')) > 32:
            raise Exception('Maximal name length is 32 bytes')

    @staticmethod
    def get_parser_name():
        return 'set-alias'

    @staticmethod
    def get_help():
        return 'Configure BSN Name'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('alias', help='Node Alias')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {'name': args.alias}
