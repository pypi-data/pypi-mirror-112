from SCA11H.commands.base.PostCommand import PostCommand
from SCA11H.commands.bcg.Direction import Direction
from SCA11H.commands.base import enum_from_value


class SetDirection(PostCommand):
    """ Configure BCG Measurement Direction """

    def __init__(self, direction: Direction, **kwargs):
        super().__init__(endpoint='/bcg/dir', payload='{"dir":%d}' % direction.value, **kwargs)

    @staticmethod
    def get_parser_name():
        return 'set-bcg-dir'

    @staticmethod
    def get_help():
        return 'Configure BCG Measurement Direction'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('direction', choices=[str(x.value) for x in Direction],
                            help='BCG measurement direction; 0 - Inverted. 1 - Normal')

    @staticmethod
    def parse_arguments(args) -> dict:
        return {'direction': enum_from_value(Direction, int(args.direction))}
