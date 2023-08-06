from enum import Enum

from SCA11H.commands.base.GetCommand import GetCommand
from SCA11H.commands.system.NetworkSecurityType import NetworkSecurityType
from SCA11H.commands.base import enum_from_value


class NetworkType(Enum):
    Station = 'sta'
    AccessPoint = 'ap'


class ActiveNetworkInfo:
    def __init__(self, network_type: NetworkType, payload):
        self.network_type = network_type
        self.ssid = payload['ssid']
        self.security = enum_from_value(NetworkSecurityType, payload['security'])
        self.password = payload.get('passphrase', None)
        self.channel = payload.get('channel', 11)
        self.dhcp_client_enabled = payload.get('dhcp', None)
        self.dhcp_server_enabled = payload.get('dhcpd', None)
        self.ip = payload.get('ip', None)
        self.netmask = payload.get('netmask', None)
        self.gateway = payload.get('gateway', None)
        self.dns_1 = payload.get('ipdns1', None)
        self.dns_2 = payload.get('ipdns2', None)

    def __str__(self):
        return '\n'.join(self.as_list())

    def as_list(self):
        res = [
            'Type:        %s' % self.network_type.name,
            'SSID:        %s' % self.ssid,
            'Security:    %s' % self.security.value,
            'Channel:     %s' % self.channel,
        ]

        def add_field(fmt, value_test, value_text=None):
            if value_test is not None:
                nonlocal res
                res.append(fmt % (value_text if value_text is not None else value_test))

        add_field('Password:    %s', self.password)
        add_field('DHCP Client: %s', self.dhcp_client_enabled, 'On' if self.dhcp_client_enabled else 'Off')
        add_field('DHCP Server: %s', self.dhcp_server_enabled, 'On' if self.dhcp_server_enabled else 'Off')
        add_field('IP Address:  %s', self.ip)
        add_field('Subnet Mask: %s', self.netmask)
        add_field('Gateway:     %s', self.gateway)
        add_field('DNS #1:      %s', self.dns_1)
        add_field('DNS #2:      %s', self.dns_2)
        return res


class GetActiveNetworkInfo(GetCommand):
    """ Query Current Network Info """

    def __init__(self, **kwargs):
        super().__init__(endpoint='/sys/netinfo', **kwargs)

    def run(self, **kwargs) -> ActiveNetworkInfo:
        res = super().run()
        for nt in NetworkType:
            if nt.value in res:
                return ActiveNetworkInfo(network_type=nt, payload=res[nt.value])

        raise Exception('Could not find active network information entry')

    @staticmethod
    def get_parser_name():
        return 'get-net-info'

    @staticmethod
    def get_help():
        return 'Query Current Network Info'
