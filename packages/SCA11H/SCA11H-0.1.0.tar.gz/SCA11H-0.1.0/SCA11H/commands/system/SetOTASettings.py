from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.system.OTASettings import OTASettings


class SetOTASettings(PostCommand):
    """ Configure OTA Settings """

    def __init__(self, settings: OTASettings, **kwargs):
        super().__init__(endpoint='/sys/ota', payload=settings.to_payload(), **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-ota-settings'

    @staticmethod
    def get_help():
        return 'Configure OTA Settings'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--enable', dest='is_enabled', action='store_true',
                            help='Enable auto-upgrade firmware from server')
        parser.add_argument('--disable', dest='is_enabled', action='store_false',
                            help='Disable auto-upgrade firmware from server')
        parser.add_argument('--url', default='', help='OTA server URL')
        parser.add_argument('--ota-username', default='', help='Username to access OTA server')
        parser.add_argument('--ota-password', default='', help='Password to access OTA server')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {
            'settings': OTASettings(enable_auto_upgrade=args.is_enabled, ota_server_url=args.url,
                                    username=args.ota_username, new_password=args.ota_password)
        }
