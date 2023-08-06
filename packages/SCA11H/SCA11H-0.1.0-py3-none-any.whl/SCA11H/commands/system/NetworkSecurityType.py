from enum import Enum


class NetworkSecurityType(Enum):
    Open = 'Open'
    WEP = 'WEP'
    WPA2_PSK = 'WPA2 PSK'
    WPA = 'WPA/WPA2 PSK'
    Unknown = 'Unknown'
