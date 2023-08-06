from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.system.NetworkSecurityType import NetworkSecurityType
from SCA11H.commands.base import enum_from_value


class NetworkInfo:
    def __init__(self, payload):
        self.ssid = payload[0]
        self.bssid = payload[1]
        self.security = enum_from_value(NetworkSecurityType, payload[2])
        self.channel = payload[3]
        self.signal_strength = payload[4]

    def __str__(self):
        return '\n'.join(self.as_list())

    def as_list(self):
        return [
            'SSID:     %s' % self.ssid,
            'BSSID:    %s' % self.bssid,
            'Security: %s' % self.security.value,
            'Channel:  %s' % self.channel,
            'RSSI:     %s dBm' % self.signal_strength,
        ]


class NetworkList:
    def __init__(self, payload):
        self.networks = [NetworkInfo(payload=x) for x in payload['networks']]

    def __str__(self):
        return ('\n' + '-' * 10 + '\n').join(['%s' % x for x in self.networks])


class ScanNetworks(GetCommand):
    """ Scan networks results """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/scan', **kwargs)

    def run(self, **kwargs) -> NetworkList:
        return NetworkList(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'scan-networks'

    @staticmethod
    def get_help():
        return 'Scan networks results'
