import asyncio
import sys
import select
import threading
import time

from enum import Enum
from queue import Queue
from dvenv import log
from dvenv.transact import Commands, Response
from collections import namedtuple

Command = namedtuple("Command", "id cmd")


class ChannelCommand(Enum):
    PYTHON_INTERACTIVE = Command(id=0, cmd=["python", "-i"])
    PYTHON = Command(id=1, cmd=["python"])
    PIP = Command(id=2, cmd=["pip"])
    CREATE_ENV = Command(id=3, cmd=["virtualenv", "-p"])


BUFFER_ORDER = ["stdout", "stderr"]
CARRIAGE_RETURN = "\r\n"
TIMEOUT = 0.01


class ChannelManager:
    def __init__(self, *, channel_id, broker) -> None:
        self.channel_id = channel_id
        self.broker = broker
        self.worker = ChannelWorker()
        self.running_process = False

        log.action(f"Initialized channel manager on: {self.channel_id}")

    def on_message(self, msg):
        cmd_id = msg["cmd_id"]

        if cmd_id == Commands.CREATE_ENV:
            log.action("Received CREATE_ENV command")

            python_version = msg["data"]["python_version"]
            path = msg["data"]["path"]

            self.running_process = True
            self.worker.run(ChannelCommand.CREATE_ENV, python_version, path)

            # if self.environments >= self.max_environments:
            #     log.warn("No availability, rejecting CREATE_ENV")

            #     response = Response(
            #         cmd_id=Commands.INIT, data={"error": RequestError.NO_AVAILABILITY}
            #     )

            #     return self.broker.send_response(response, topic=self.channel_id)

        elif cmd_id == Commands.RUN:
            log.action("Received RUN command")

            channel_command = msg["data"]["channel_command"]
            args = msg["data"]["args"]

            if self.running_process and self.worker.active_process:
                self.worker.active_process.terminate()

            if channel_command == list(ChannelCommand.PYTHON_INTERACTIVE.value):
                self.worker.run(ChannelCommand.PYTHON_INTERACTIVE, *args)
                self.running_process = True
            elif channel_command == list(ChannelCommand.PYTHON.value):
                self.worker.run(ChannelCommand.PYTHON, *args)
                self.running_process = True
            else:
                pass

        elif cmd_id == Commands.PROCESS_INPUT:
            self.worker.send_line(line=msg["data"]["input"])

    def kill(self):
        if self.worker.active_process:
            self.worker.active_process.terminate()
            self.worker.reset()
            self.running_process = False

    def status(self):
        pass

    def process(self):
        reset = False
        return_code = None

        if self.worker.active_process:
            process_status = self.worker.process_status()

            if process_status is not None:
                return_code = process_status
                reset = True

            output = self.worker.get_output()

            if output != "":
                response = Response(
                    cmd_id=Commands.PROCESS_OUTPUT,
                    data={"output": output},
                )

                self.broker.send_response(response, topic=self.channel_id)

        if reset:
            response = Response(
                cmd_id=Commands.PROCESS_EXIT,
                data={"return_code": return_code},
            )

            self.broker.send_response(response, topic=self.channel_id)
            self.worker.reset()


class ChannelWorker:
    def __init__(self) -> None:
        self.reset()

    async def _read_stream(self, proc, stream, out_queue):
        timeout = TIMEOUT

        while True:
            try:
                c = await asyncio.wait_for(stream.read(1), timeout)
            except asyncio.TimeoutError:
                c = None

            if c:
                out_queue.put(c.decode())

            if proc.returncode is not None:
                break

    def _write_stream(self, proc, stream):
        timeout = TIMEOUT

        while proc.returncode is None:
            input, _, _ = select.select([sys.stdin], [], [], timeout)

            if input:
                line = sys.stdin.readline().rstrip() + CARRIAGE_RETURN
                stream.write(line.encode("utf-8"))

    async def _async_callback(self, cmd, proc_queue, stdout_queue, stderr_queue, *args):
        extra_args = list(args[0])

        proc = await asyncio.create_subprocess_exec(
            *cmd.value.cmd,
            *extra_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )

        proc_queue.put(proc)

        await asyncio.wait(
            [
                self._read_stream(proc, proc.stdout, stdout_queue),
                self._read_stream(proc, proc.stderr, stderr_queue),
            ]
        )

        return await proc.wait()

    def _flush_queue(self, queue):
        data = []

        while not queue.empty():
            c = queue.get()
            data.append(c)

        return data

    def _spawn_async(self, cmd, proc_queue, stdout_queue, stderr_queue, *args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            self._async_callback(cmd, proc_queue, stdout_queue, stderr_queue, args)
        )
        loop.close()

    def run(self, cmd, *args):
        log.action(f"Running: {cmd}")

        self.proc_queue = Queue()
        self.stdout_queue = Queue()
        self.stderr_queue = Queue()

        self.read_thread = threading.Thread(
            target=self._spawn_async,
            args=(cmd, self.proc_queue, self.stdout_queue, self.stderr_queue, *args),
        )
        self.read_thread.daemon = True
        self.read_thread.start()

        self.active_process = self.proc_queue.get()

    def reset(self):
        self.read_thread = None
        self.active_process = None
        self.proc_queue = None
        self.stdout_queue = None
        self.stderr_queue = None

    def send_line(self, *, line):
        if self.active_process is not None:
            line = line.rstrip() + CARRIAGE_RETURN
            self.active_process.stdin.write(line.encode("utf-8"))

    def process(self):
        data = []

        if BUFFER_ORDER[0] == "stderr":
            data = self._flush_queue(self.stderr_queue)
            data.extend(self._flush_queue(self.stdout_queue))
        elif BUFFER_ORDER[0] == "stdout":
            data = self._flush_queue(self.stdout_queue)
            data.extend(self._flush_queue(self.stderr_queue))

        return data

    def get_output(self):
        data = self.process()
        output_str = "".join(data)
        return output_str

    def wait_for_completion(self):
        if self.active_process is not None:

            self.read_thread.join()
            return_code = self.active_process.returncode
            self.reset()

            return return_code

    def process_status(self):
        if self.active_process is not None:
            if self.active_process.returncode is not None:
                return self.active_process.returncode
