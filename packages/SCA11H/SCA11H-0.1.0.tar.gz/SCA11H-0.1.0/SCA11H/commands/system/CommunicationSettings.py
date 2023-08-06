from enum import Enum
from typing import Optional

from SCA11H.commands.base import enum_from_value


class CommunicationMode(Enum):
    Cloud = 1
    Local = 0


class CommunicationSettings:
    def __init__(self, mode: CommunicationMode, enable_https: Optional[bool] = None, server_url: Optional[str] = None,
                 username: Optional[str] = None, new_password: Optional[str] = None,
                 report_interval: Optional[int] = None,
                 network_id: Optional[str] = None, node_id: Optional[str] = None, reset_interval: Optional[int] = None):
        if mode == CommunicationMode.Cloud and (
                enable_https is None or server_url is None or username is None or new_password is None or
                report_interval is None or network_id is None or node_id is None or reset_interval is None):
            raise Exception('Cloud mode requires all "optional" parameters')

        if report_interval is not None and (report_interval < 5 or report_interval > 90):
            raise Exception('Number of samples in one XML-message should be between 5 and 90')

        self.mode = mode
        self.enable_https = enable_https
        self.server_url = server_url
        self.username = username
        self.new_password = new_password
        self.report_interval = report_interval
        self.network_id = network_id
        self.node_id = node_id
        self.reset_interval = reset_interval

    @staticmethod
    def from_payload(payload):
        return CommunicationSettings(mode=enum_from_value(CommunicationMode, payload['mode']),
                                     enable_https=payload['https_enable'], server_url=payload['url'],
                                     username=payload['username'], report_interval=payload['report_interval'],
                                     network_id=payload['network_id'], node_id=payload['node_id'],
                                     reset_interval=payload['reset_interval'])

    def as_list(self):
        res = [
            'Mode:            %s' % self.mode.name,
        ]

        def add_field(fmt, value_test, value_text=None):
            if value_test is not None:
                nonlocal res
                res.append(fmt % (value_text if value_text is not None else value_test))

        add_field('HTTPS:           %s', self.enable_https, 'On' if self.enable_https else 'Off')
        add_field('Cloud URL:       %s', self.server_url)
        add_field('Cloud Username:  %s', self.username)
        add_field('Cloud Password:  %s', self.new_password)
        add_field('Report Interval: %s', self.report_interval)
        add_field('Network Group:   %s', self.network_id)
        add_field('Node Identifier: %s', self.node_id)
        add_field('Reset Interval:  %s', self.reset_interval)
        return res

    def __str__(self):
        return '\n'.join(self.as_list())
