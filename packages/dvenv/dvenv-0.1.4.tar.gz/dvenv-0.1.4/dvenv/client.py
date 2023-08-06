import time
import json
import sys
import select

from uuid import uuid4
from dvenv.broker import RedisBroker
from dvenv.transact import Request, Commands, RequestError
from dvenv.channel import ChannelCommand
from dvenv import log

CARRIAGE_RETURN = "\r\n"
TIMEOUT = 0.001


class Client:
    def __init__(self, *, cfg, **additional_cfg) -> None:
        self.cfg = {**cfg, **additional_cfg}
        self.broker = RedisBroker(
            host=self.cfg["broker_host"],
            port=self.cfg["broker_port"],
            request_timeout=self.cfg["request_timeout"],
            response_timeout=self.cfg["response_timeout"],
            username=self.cfg["broker_username"],
            password=self.cfg["broker_password"],
        )

        self.client_id = str(uuid4())
        self.channel_id = self._get_channel_id()
        self.broker.subscribe(self.channel_id)

        self.msg_backlog = []

    def _get_channel_id(self):
        if self.cfg.get("broker_channel_id"):
            return self.cfg.get("broker_channel_id")
        else:
            return str(uuid4())

    def initialize_channel(self):
        req = Request(
            cmd_id=Commands.INIT,
            data={
                "client_id": self.client_id,
                "channel_id": self.channel_id,
            },
        )
        self.broker.send_request(req)

        response = self._wait_for_response(
            cmd_id=Commands.INIT, timeout=self.cfg["response_timeout"]
        )

        if response is None:
            log.die("No response received from broker")

        response_data = response.get("data")
        if response_data == {}:
            log.action("INIT request accepted")
        elif response_data.get("error") == RequestError.NO_AVAILABILITY:
            log.die("INIT request rejected: server is at capacity")

    def create_new_environment(
        self,
        *,
        python_version,
        path,
    ):
        req = Request(
            cmd_id=Commands.CREATE_ENV,
            data={
                "client_id": self.client_id,
                "channel_id": self.channel_id,
                "python_version": python_version,
                "path": path,
            },
        )
        self.broker.send_message(req, topic=self.channel_id)
        return self._enter_interactive_process()

    def run_python(self, *args):
        req = None

        if len(args) == 0:
            req = Request(
                cmd_id=Commands.RUN,
                data={
                    "channel_command": ChannelCommand.PYTHON_INTERACTIVE.value,
                    "args": list(args),
                    "client_id": self.client_id,
                    "channel_id": self.channel_id,
                },
            )
        else:
            req = Request(
                cmd_id=Commands.RUN,
                data={
                    "channel_command": ChannelCommand.PYTHON.value,
                    "args": list(args),
                    "client_id": self.client_id,
                    "channel_id": self.channel_id,
                },
            )

        self.broker.send_message(req, topic=self.channel_id)
        return self._enter_interactive_process()

    def receive_messages(self):
        response_messages = self.broker.get_messages()

        if len(response_messages) > 0:
            for message in response_messages:
                try:
                    _ = self._parse_channel_message(message["data"].decode())
                except AttributeError:
                    pass

                response_messages = self.broker.get_messages()

    def _enter_interactive_process(self):
        process_running = True
        return_code = None

        while process_running:
            self._get_input()

            response_messages = self.broker.get_messages()
            if len(response_messages) > 0:
                for message in response_messages:
                    try:
                        msg = self._parse_channel_message(message["data"].decode())

                        cmd_id = msg.get("cmd_id")
                        if cmd_id is not None and cmd_id == Commands.PROCESS_OUTPUT:
                            self._flush_output(msg)
                        elif cmd_id is not None and cmd_id == Commands.PROCESS_EXIT:
                            return_code = msg["data"]["return_code"]
                            log.action(
                                f"Process exited with return code: {return_code}",
                                prepend="\n",
                            )
                            process_running = False
                        elif cmd_id is not None and cmd_id == Commands.CREATE_ENV:
                            pass
                        else:
                            self.msg_backlog.append(self.msg_backlog)
                    except AttributeError:
                        pass

        return return_code

    def _get_input(self):
        input, _, _ = select.select([sys.stdin], [], [], TIMEOUT)

        if input:
            line = sys.stdin.readline().rstrip() + CARRIAGE_RETURN

            req = Request(
                cmd_id=Commands.PROCESS_INPUT,
                data={
                    "client_id": self.client_id,
                    "channel_id": self.channel_id,
                    "input": line,
                },
            )
            self.broker.send_message(req, topic=self.channel_id)

    def _flush_output(self, msg):
        sys.stdout.write(msg["data"]["output"])
        sys.stdout.flush()

    def _wait_for_response(self, *, cmd_id, timeout):
        start_time = time.time()
        elapsed = 0.0

        while elapsed < timeout:
            response_messages = self.broker.get_messages()

            if len(response_messages) > 0:
                for message in response_messages:
                    try:
                        msg = self._parse_channel_message(message["data"].decode())
                        cmd_id = msg.get("cmd_id")
                        if cmd_id is not None and cmd_id == cmd_id:
                            return msg
                        else:
                            self.msg_backlog.append(self.msg_backlog)
                    except AttributeError:
                        pass

            elapsed = time.time() - start_time

    def _parse_channel_message(self, msg):
        msg = json.loads(msg)
        msg_data = msg["data"]

        client_id = msg_data.get("client_id")
        if client_id is not None:
            return

        return msg
