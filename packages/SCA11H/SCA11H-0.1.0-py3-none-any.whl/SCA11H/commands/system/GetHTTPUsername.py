from SCA11H.commands.base.GetCommand import GetCommand
import sys


class GetHTTPUsername(GetCommand):
    """ Query Authentication Account (Username to access HTTP API) """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/account', **kwargs)
        print("WARNING: GetHTTPUsername didn't work upon testing and always returned -1", file=sys.stderr)

    def run(self, **kwargs) -> str:
        return super().run()['username']

    @staticmethod
    def get_parser_name():
        return 'get-username'

    @staticmethod
    def get_help():
        return 'Query Authentication Account (Username to access HTTP API)'
