from enum import Enum
from typing import Dict, Optional, Union, List
from base64 import b64encode
from http.client import HTTPConnection
import json
import argparse


class Method(Enum):
    get = 'GET'
    post = 'POST'


class Command:
    TIMEOUT = 30  # Operations timeout

    def __init__(self, host: str, username: str = 'admin', password: str = 'admin', **kwargs):
        super().__init__(**kwargs)

        self.host = host
        self.username = username
        self.password = password

    def get_headers(self) -> Dict[str, str]:
        auth_string = '{}:{}'.format(self.username, self.password)
        auth_string = auth_string.encode('utf8')
        user_and_pass = b64encode(auth_string).decode('utf8')
        return {'Authorization': 'Basic %s' % user_and_pass}

    def run(self, method: Method, endpoint: str, payload: Optional[str] = None) -> Dict[str, Union[str, int, Dict[str, str], List[Union[str, int]]]]:
        text = self.run_for_plaintext_result(method=method, endpoint=endpoint, payload=payload)
        try:
            return json.loads(text)
        except Exception as e:
            print('Error parsing the node response:\nResponse text: "%s"\nError message: "%s"' % (text, e))
            raise

    def run_for_plaintext_result(self, method: Method, endpoint: str, payload: Optional[str] = None) -> str:
        if method == Method.post and payload is None:
            raise Exception('POST method requires a payload')

        connection = HTTPConnection(self.host, timeout=Command.TIMEOUT)
        connection.request(method=method.value, url=endpoint, headers=self.get_headers(), body=payload)
        res = connection.getresponse()
        return res.read().decode('utf8')

    @staticmethod
    def get_parser_name():
        return None

    @staticmethod
    def get_help():
        return None

    @staticmethod
    def add_arguments(parser: argparse.ArgumentParser):
        pass

    @staticmethod
    def parse_arguments(args) -> dict:
        return {}
