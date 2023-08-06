import json
from typing import Optional


class OTASettings:
    def __init__(self, enable_auto_upgrade: bool, ota_server_url: str, username: str,
                 new_password: Optional[str] = None):
        if enable_auto_upgrade and (ota_server_url is None or username is None or new_password is None):
            raise Exception('OTA Settings are missing')

        if len(ota_server_url.encode('ascii')) > 128:
            raise Exception('Maximal URL length is 128 bytes')

        if len(username.encode('ascii')) > 16:
            raise Exception('Maximal username length is 16 bytes')

        if new_password is not None and len(new_password.encode('ascii')) > 16:
            raise Exception('Maximal password length is 16 bytes')

        self.enable_auto_upgrade = enable_auto_upgrade
        self.ota_server_url = ota_server_url
        self.username = username
        self.new_password = new_password

    @staticmethod
    def from_payload(payload):
        return OTASettings(enable_auto_upgrade=payload['autoupd'] == 1, ota_server_url=payload['url'],
                           username=payload['username'])

    def as_list(self):
        res = [
            'Auto Update:    %s' % ('On ' if self.enable_auto_upgrade else 'Off'),
            'OTA Server URL: %s' % (self.ota_server_url if self.ota_server_url is not None and len(self.ota_server_url) > 0 else 'None'),
            'Username:       %s' % (self.username if self.username is not None and len(self.username) > 0 else 'None'),
        ]

        if self.new_password is not None:
            res.append('New Password:   %s' % self.new_password)

        return res

    def __str__(self):
        return '\n'.join(self.as_list())

    def to_payload(self):
        res = {
            'autoupd': 1 if self.enable_auto_upgrade else 0,
            'url': self.ota_server_url,
            'username': self.username,
            'new_password': self.new_password
        }

        return json.dumps(res)
