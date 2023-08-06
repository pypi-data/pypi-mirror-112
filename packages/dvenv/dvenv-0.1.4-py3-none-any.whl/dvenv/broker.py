import redis

from abc import ABC, abstractmethod
from dvenv import log
from dvenv.transact import REQUEST_QUEUE_TOPIC


class Broker(ABC):
    def __init__(
        self, *, host, port, request_timeout, response_timeout, username, password
    ) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.request_timeout = request_timeout
        self.response_timeout = response_timeout
        self.username = username
        self.password = password

    @abstractmethod
    def send_request(self, request):
        pass

    @abstractmethod
    def send_message(self, request, topic):
        pass

    @abstractmethod
    def send_response(self, response, topic):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def subscribe(self, topic):
        pass

    @abstractmethod
    def get_messages(self):
        pass


class RedisBroker(Broker):
    def __init__(
        self, *, host, port, request_timeout, response_timeout, username, password
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            request_timeout=request_timeout,
            response_timeout=response_timeout,
            username=username,
            password=password,
        )

        self.broker_backend = "redis"

        log.action("********************************")
        log.action(f"BROKER: {self.broker_backend}")
        log.action(f"HOST: {self.host}")
        log.action(f"PORT: {self.port}")
        log.action(f"REQUEST TIMEOUT: {self.request_timeout}")
        log.action(f"RESPONSE TIMEOUT: {self.response_timeout}")
        log.action("********************************")

        self._connect()

    def _connect(self):
        self.r = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=0,
            username=self.username,
            password=self.password,
        )

        if not self.is_connected():
            log.die(f"Unable to connect to broker: redis@{self.host}/{self.port}")

        log.info(f"Connected to broker: redis@{self.host}/{self.port}")
        self.ps = self.r.pubsub()

    def is_connected(self):
        try:
            self.r.ping()
        except redis.exceptions.ConnectionError:
            return False

        return True

    def send_request(self, request):
        payload = request.serialize()
        self.r.publish(REQUEST_QUEUE_TOPIC, payload)

    def send_message(self, request, topic):
        payload = request.serialize()
        self.r.publish(topic, payload)

    def send_response(self, response, topic):
        payload = response.serialize()
        self.r.publish(topic, payload)

    def subscribe(self, topic):
        return self.ps.subscribe(topic)

    def get_messages(self):
        messages = []

        message = self.ps.get_message()
        while message is not None:
            messages.append(message)
            message = self.ps.get_message()

        return messages
