from enum import Enum
import json

from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.base import enum_from_value


class Command(Enum):
    Reboot = 'reboot'  # Reboots the system
    Restore = 'restore'  # Restore system's factory settings and reboot the system


class RunCommand(PostCommand):
    """ Run a system command """

    def __init__(self, command: Command, **kwargs):
        super().__init__(endpoint='/sys/cmd',
                         payload=json.dumps({"cmd": command.value}),
                         **kwargs)

    @staticmethod
    def get_parser_name():
        return 'run-command'

    @staticmethod
    def get_help():
        return 'Run a system command'

    @staticmethod
    def add_arguments(parser):
        subparsers = parser.add_subparsers(title='sys-command', dest='sys_command', help='System Command to run')
        subparsers.add_parser(Command.Reboot.value, help='Reboots the system')
        subparsers.add_parser(Command.Restore.value, help="Restore system's factory settings and reboot the system")

    @staticmethod
    def parse_arguments(args) -> dict:
        if args.sys_command is None:
            raise Exception('Missing required argument: sys-command')

        return {'command': enum_from_value(Command, args.sys_command)}
