from enum import Enum
import json

from SCA11H.commands.base.PostCommand import PostCommand


class Command(Enum):
    # Restore BCG factory settings.(BCG parameters, direction and running mode)
    Restore = ('restore', 'restore')

    # Restore default BCG parameters
    SetDefaultParameters = ('set_default_pars', 'reset-parameters')


class RunCommand(PostCommand):
    """ Run a BCG command """

    def __init__(self, command: Command, **kwargs):
        super().__init__(endpoint='/bcg/cmd',
                         payload=json.dumps({"cmd": command.value[0]}),
                         **kwargs)

    @staticmethod
    def get_parser_name():
        return 'run-bcg-command'

    @staticmethod
    def get_help():
        return 'Run a BCG command'

    @staticmethod
    def add_arguments(parser):
        subparsers = parser.add_subparsers(title='bcg-command', dest='bcg_command', help='BCG Command to run')
        subparsers.add_parser(Command.Restore.value[1],
                              help='Restore BCG factory settings.(BCG parameters, direction and running mode)')
        subparsers.add_parser(Command.SetDefaultParameters.value[1], help='Restore default BCG parameters')

    @staticmethod
    def parse_arguments(args) -> dict:
        if args.bcg_command is None:
            raise Exception('Missing required argument: bcg-command')
        elif args.bcg_command == Command.Restore.value[1]:
            command = Command.Restore
        elif args.bcg_command == Command.SetDefaultParameters.value[1]:
            command = Command.SetDefaultParameters
        else:
            raise Exception('Invalid argument: bcg-command')

        return {'command': command}
