import json

from enum import IntEnum
from uuid import uuid4

REQUEST_QUEUE_TOPIC = "request_queue"


class Commands(IntEnum):
    INIT = 0
    CREATE_ENV = 1
    DELETE = 2
    RUN = 3
    PROCESS_INPUT = 4
    PROCESS_OUTPUT = 5
    PROCESS_EXIT = 6


class RequestResponseType(IntEnum):
    SYNC = 0
    ASYNC = 1


class RequestError(IntEnum):
    NO_AVAILABILITY = 1


class Request:
    def __init__(self, *, cmd_id, data) -> None:
        self.id = str(uuid4())[:8]
        self.cmd_id = cmd_id
        self.data = data

    def serialize(self):
        payload = {"id": self.id, "cmd_id": self.cmd_id, "data": self.data}
        return json.dumps(payload)


class Response:
    def __init__(self, *, cmd_id, data) -> None:
        self.id = str(uuid4())[:8]
        self.cmd_id = cmd_id
        self.data = data

    def serialize(self):
        payload = {"id": self.id, "cmd_id": self.cmd_id, "data": self.data}
        return json.dumps(payload)
