from SCA11H.commands.base.GetCommand import GetCommand


class FirmwareVersions:
    def __init__(self, payload):
        self.file_system_version = payload['fs_ver']
        self.backup_file_system_version = payload['bfs_ver']
        self.main_firmware_version = payload['fw_ver']
        self.backup_main_firmware_version = payload['bfw_ver']
        self.device_configuration_table_version = payload['dct_ver']
        self.backup_device_configuration_table_version = payload['bdct_ver']
        self.wlan_firmware_version = payload['wlan_ver']
        self.bootloader_firmware_version = payload['boot_ver']
        self.ota_recovery_firmware_version = payload['ota_ver']

    def __str__(self):
        return '\n'.join(self.as_list())

    def as_list(self):
        return [
            'FS Version:   %s' % self.file_system_version,
            'BFS Version:  %s' % self.backup_file_system_version,
            'FW Version:   %s' % self.main_firmware_version,
            'BFW Version:  %s' % self.backup_main_firmware_version,
            'DCT Version:  %s' % self.device_configuration_table_version,
            'BDCT Version: %s' % self.backup_device_configuration_table_version,
            'WLAN Version: %s' % self.wlan_firmware_version,
            'Boot Version: %s' % self.bootloader_firmware_version,
            'OTA Version:  %s' % self.ota_recovery_firmware_version
        ]


class GetFirmwareInfo(GetCommand):
    """ Query All Firmware Info """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/fwinfo', **kwargs)

    def run(self, **kwargs) -> FirmwareVersions:
        return FirmwareVersions(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-sys-firmware-info'

    @staticmethod
    def get_help():
        return 'Query All Firmware Info'
