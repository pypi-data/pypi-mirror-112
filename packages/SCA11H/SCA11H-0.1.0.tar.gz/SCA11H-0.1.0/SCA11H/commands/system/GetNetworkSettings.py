from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.system.NetworkSecurityType import NetworkSecurityType
from SCA11H.commands.base import enum_from_value


class SettingsEntry:
    def __init__(self, payload):
        self.ssid = payload['ssid']
        self.security = enum_from_value(NetworkSecurityType, payload['security'])
        self.password = payload['passphrase']
        self.channel = payload.get('channel', 11)
        self.dhcp_client_enabled = payload.get('dhcp', None)
        self.dhcp_server_enabled = payload.get('dhcpd', None)
        self.static_ip = payload.get('ip', None)
        self.static_netmask = payload.get('netmask', None)
        self.static_gateway = payload.get('gateway', None)
        self.static_dns_1 = payload.get('ipdns1', None)
        self.static_dns_2 = payload.get('ipdns2', None)

    def __str__(self):
        return '\n'.join(self.as_list())

    def as_list(self):
        res = [
            'SSID:           %s' % self.ssid,
            'Security:       %s' % self.security.value,
            'Password:       %s' % self.password,
            'Channel:        %s' % self.channel,
        ]

        def add_field(fmt, value_test, value_text=None):
            if value_test is not None:
                nonlocal res
                res.append(fmt % (value_text if value_text is not None else value_test))

        add_field('DHCP Client:    %s', self.dhcp_client_enabled, 'On' if self.dhcp_client_enabled else 'Off')
        add_field('DHCP Server:    %s', self.dhcp_server_enabled, 'On' if self.dhcp_server_enabled else 'Off')
        add_field('Static IP:      %s', self.static_ip)
        add_field('Static Netmask: %s', self.static_netmask)
        add_field('Static Gateway: %s', self.static_gateway)
        add_field('Static DNS #1:  %s', self.static_dns_1)
        add_field('Static DNS #2:  %s', self.static_dns_2)

        return res


class SettingsBundle:
    def __init__(self, payload):
        self.soft_ap = SettingsEntry(payload=payload['ap'])
        self.station = SettingsEntry(payload=payload['sta'])

    def as_list(self):
        return [
            'Soft AP:',
            '\n'.join('   %s' % x for x in self.soft_ap.as_list()),
            'Station:',
            '\n'.join('   %s' % x for x in self.station.as_list()),
        ]

    def __str__(self):
        return '\n'.join(self.as_list())


class GetNetworkSettings(GetCommand):
    """ Query Network Settings """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/network', **kwargs)

    def run(self, **kwargs) -> SettingsBundle:
        return SettingsBundle(payload=super().run())

    @staticmethod
    def get_parser_name():
        return 'get-net-settings'

    @staticmethod
    def get_help():
        return 'Query Network Settings'
