from SCA11H.commands.base.Command import Command, Method
from typing import Dict, Union
import json


class PostResult:
    def __init__(self, payload: Dict[str, Union[str, int, Dict[str, str]]]):
        self.errno = int(payload['errno'])

    def __str__(self):
        return json.dumps(self.__dict__)

    def __bool__(self):
        return self.errno == 0

    def check(self):
        if self.errno != 0:
            raise Exception('Node response error: %s' % self.errno)


class PostCommand(Command):
    def __init__(self, endpoint: str, payload: str, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = endpoint
        self.payload = payload

    def run(self, checked: bool = True, **kwargs) -> PostResult:
        result = PostResult(payload=super().run(method=Method.post, endpoint=self.endpoint, payload=self.payload))
        if checked:
            result.check()

        return result

    def run_for_plaintext_result(self, **kwargs) -> str:
        return super().run_for_plaintext_result(method=Method.post, endpoint=self.endpoint, payload=self.payload)
