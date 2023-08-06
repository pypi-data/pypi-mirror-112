import time
import json

from dvenv.broker import RedisBroker
from dvenv.transact import Response, Commands, RequestError, REQUEST_QUEUE_TOPIC
from dvenv.channel import ChannelManager
from dvenv import log


BROKER_SLEEP_TIME = 0.001


class Server:
    def __init__(self, *, cfg) -> None:
        log.action("Starting dvenv server")

        self.broker = RedisBroker(
            host=cfg["broker_host"],
            port=cfg["broker_port"],
            request_timeout=cfg["request_timeout"],
            response_timeout=cfg["response_timeout"],
            username=cfg["broker_username"],
            password=cfg["broker_password"],
        )

        self.environment_path = cfg["environment_path"]
        self.channels = {}
        self.environments = 0
        self.max_channels = 10  # TODO: add to dvenv config file
        self.max_environments = cfg["max_environments"]

    def run(self):
        self.broker.subscribe(REQUEST_QUEUE_TOPIC)

        while self.broker.is_connected():
            messages = self.broker.get_messages()
            for message in messages:
                log.debug(f"Received message: {message}")
                self._handle_message(message)

            for channel_id in self.channels.keys():
                self.channels[channel_id].process()

            time.sleep(BROKER_SLEEP_TIME)

    def _handle_message(self, message):
        channel_id = message["channel"].decode()
        if channel_id == REQUEST_QUEUE_TOPIC:
            try:
                self._handle_request(message["data"].decode())
            except AttributeError:
                pass
        elif channel_id in self.channels.keys():
            try:
                self._handle_channel_message(channel_id, message["data"].decode())
            except AttributeError:
                pass
        else:
            log.warn(f"Unhandled message: {message}")

    def _handle_request(self, request_data):
        request_data = json.loads(request_data)
        cmd_id = request_data["cmd_id"]
        channel_id = str(request_data["data"]["channel_id"])

        if cmd_id == Commands.INIT:
            log.action("Received INIT request")

            if len(self.channels.keys()) >= self.max_channels:
                log.warn("Rejected INIT request: No availability")

                response = Response(
                    cmd_id=Commands.INIT, data={"error": RequestError.NO_AVAILABILITY}
                )
                return self.broker.send_response(response, topic=channel_id)

            else:
                log.action("Accepted INIT request")
                response = Response(cmd_id=Commands.INIT, data={})

                if channel_id not in self.channels.keys():
                    log.action(f"Opening new channel: {channel_id}")
                    self.channels[channel_id] = ChannelManager(
                        channel_id=channel_id, broker=self.broker
                    )
                    self.broker.subscribe(channel_id)

                return self.broker.send_response(response, topic=channel_id)

    def _handle_channel_message(self, channel_id, msg):
        msg = json.loads(msg)
        msg_data = msg.get("data")

        client_id = msg_data.get("client_id")
        if client_id is None:
            return

        self.channels[channel_id].on_message(msg)
