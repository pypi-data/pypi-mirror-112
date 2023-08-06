from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.system.CommunicationSettings import CommunicationSettings, CommunicationMode


class SetCommunicationSettings(PostCommand):
    """ Configure Communication Settings """

    def __init__(self, settings=CommunicationSettings, **kwargs):
        super().__init__(endpoint='/sys/comm', payload='%s' % settings, **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-comm-settings'

    @staticmethod
    def get_help():
        return 'Configure Communication Settings'

    @staticmethod
    def add_arguments(parser):
        subparsers = parser.add_subparsers(title='mode', dest='mode', help='Communication mode')
        subparsers.add_parser('local', help='Local Mode')  # It has no arguments

        cloud = subparsers.add_parser('cloud', help='Cloud Mode')
        cloud.add_argument('--with-https', action='store_true', required=True, help='Enable HTTPS communication')
        cloud.add_argument('--url', required=True, help='Cloud server URL')
        cloud.add_argument('--cloud-username', required=True, help='Username to access cloud server')
        cloud.add_argument('--cloud-password', required=True, help='Password to access cloud server')
        cloud.add_argument('--report-interval', type=int, required=True,
                           help='Number of samples in one XML-message')
        cloud.add_argument('--network-group', required=True, help='Identification of network group')
        cloud.add_argument('--node-id', required=True, help='Identification of BCG Sensor Node')
        cloud.add_argument('--reset-interval', required=True, type=int,
                           help='Seconds between two consecutive timesync/BCG timestamp reset. Must be divisible by '
                                '"report_interval"')

    @staticmethod
    def parse_arguments(args) -> dict:
        if args.mode is None:
            raise Exception('Missing required argument: mode')

        if args.mode == 'local':
            return {'settings': CommunicationSettings(mode=CommunicationMode.Local)}

        return {
            'settings': CommunicationSettings(mode=CommunicationMode.Cloud,
                                              enable_https=args.with_https,
                                              server_url=args.url,
                                              username=args.cloud_username,
                                              new_password=args.cloud_password,
                                              report_interval=args.report_interval,
                                              network_id=args.network_group,
                                              node_id=args.node_id,
                                              reset_interval=args.reset_interval)
        }
