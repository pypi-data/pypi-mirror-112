from SCA11H.commands.base.GetCommand import GetCommand
from typing import Dict


class SystemInfo:
    def __init__(self, payload: Dict[str, str]):
        self.uuid = payload['uuid']
        self.name = payload['name']
        self.alias = payload['alias']
        self.main_firmware_version = payload['fw_ver']
        self.wlan_firmware_version = payload['wlan_ver']
        self.file_system_version = payload['fs_ver']

    def __str__(self):
        return '\n'.join(self.as_list())

    def as_list(self):
        return [
            'UUID:         %s' % self.uuid,
            'Name:         %s' % self.name,
            'Alias:        %s' % self.alias,
            'Main Version: %s' % self.main_firmware_version,
            'WLAN Version: %s' % self.wlan_firmware_version,
            'FS Version:   %s' % self.file_system_version,
        ]


class GetBasicInfo(GetCommand):
    """ Query Basic System Info """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys', **kwargs)

    def run(self, **kwargs) -> SystemInfo:
        return SystemInfo(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-sys-info'

    @staticmethod
    def get_help():
        return 'Query Basic System Info'
