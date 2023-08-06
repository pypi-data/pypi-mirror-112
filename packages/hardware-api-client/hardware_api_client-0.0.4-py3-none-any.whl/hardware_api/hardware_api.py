#!/usr/bin/env python3
#
# TODO: Could we implement the sd card to be compatible with pyfilesystem.org?

import base64
import io
import json
import os
import queue
import re
import sys
import threading
import time
from urllib.parse import urlparse

import requests
import websocket


def _geturl(server):
    url = server.geturl()
    if url[-1] == "/":
        url = url[:-1]
    return url


def _get_json(server, api_token, path):
    if path[0] == "/":
        path = path[1:]
    full_path = _geturl(server) + "/" + path
    params = {"api_token": api_token}
    r = requests.get(full_path, params=params, allow_redirects=False)
    if r.status_code < 200 or r.status_code >= 300:
        raise Exception("Invalid status code {}: {}".format(r.status_code, r.text))
    return r.json()


def _post_json(server, api_token, path, json_struct):
    if path[0] == "/":
        path = path[1:]
    full_path = _geturl(server) + "/" + path
    params = {"api_token": api_token}
    r = requests.post(full_path, params=params, data=json.dumps(json_struct), allow_redirects=False)
    if r.status_code < 200 or r.status_code >= 300:
        raise Exception("Invalid status code {}: {}".format(r.status_code, r.text))
    return r.json()


class HardwareAPI:
    def __init__(self, api_token, server="https://hardware-api.com/"):
        self.server = urlparse(server)
        self.api_token = api_token

    def ListDevices(self):
        return _get_json(self.server, self.api_token, "/api/v1/devices")

    def User(self):
        return _get_json(self.server, self.api_token, "/api/v1/user")


class HardwareAPIDevice:
    def __init__(self, device_name, api_token, server="https://hardware-api.com/"):
        self.device_name = device_name
        self.api_token = api_token
        self.server = urlparse(server)

    def _get_json(self, path):
        return _get_json(self.server, self.api_token, "api/v1/{}/{}".format(self.device_name, path))

    def _post_json(self, path, json_struct):
        return _post_json(
            self.server,
            self.api_token,
            "/api/v1/{}/{}".format(self.device_name, path),
            json_struct,
        )

    def list_relays(self):
        return list(self._get_json("relay").keys())

    def get_serial(self, serial_name, replay=False):
        return HardwareAPISerial(
            self.device_name, self.api_token, serial_name, self.server.geturl(), replay
        )

    def get_relay(self, relay_name):
        return HardwareAPIRelay(self.device_name, self.api_token, relay_name, self.server.geturl())

    def get_sdwire(self, sdwire_name):
        return HardwareAPISDWire(
            self.device_name, self.api_token, sdwire_name, self.server.geturl()
        )

    def list_tftp_files(self):
        return self._get_json("tftp")

    def add_tftp_url(self, name, remote_url):
        """add_tftp_url adds an HTTP/HTTPS url as a TFTP target for the device"""
        return self._post_json("tftp", {name: remote_url})

    def add_tftp_file(self, name, local_file):
        """add_tftp_file uploads a local file to the server to be made accessible
        to the device as the given name via tftp"""
        remotefile = os.path.basename(local_file)
        full_path = _geturl(self.server) + "/api/v1/{}/tftp".format(self.device_name)
        params = {"api_token": self.api_token}
        files = {"uploadfile": (remotefile, open(local_file, "rb"), "application/binary")}
        data = {"name": name}
        r = requests.post(full_path, params=params, files=files, data=data)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception("Unable to upload file: {}".format(r.status_code))

    def get_summary(self):
        return self._get_json("summary")


class HardwareAPISerial:
    """Matches the Pyserial API"""

    def __init__(
        self,
        device_name,
        api_token,
        serial_name,
        server="https://hardware-api.com",
        replay=False,
    ):
        self._device_name = device_name
        self._server = urlparse(server)
        self._buffer = queue.Queue()
        self._opened = False
        self._api_token = api_token
        self._name = device_name + "/serial/" + serial_name

        if self._server.scheme == "http":
            scheme = "ws"
        else:
            scheme = "wss"

        full_path = "{}://{}/api/v1/{}?api_token={}".format(
            scheme, self._server.netloc, self._name, api_token
        )
        if replay:
            full_path += "&replay=1"
        self._ws = websocket.WebSocketApp(
            full_path,
            on_message=lambda ws, message: self._add_message(ws, message),
            on_error=lambda ws, error: self._on_error(ws, error),
            on_close=lambda ws: self._on_close(ws),
            on_open=lambda ws: self._on_open(ws),
        )
        self._thread = threading.Thread(target=self._ws.run_forever, args=())
        self._thread.daemon = True
        self._thread.start()
        self.timeout = 1

    def _on_close(self, socket):
        self._opened = False

    def _on_open(self, socket):
        self._opened = True

    def _on_error(self, socket, error):
        print("ws error", error)

    def _add_message(self, socket, message):
        try:
            # TODO: Should be just dealing in raw bytes, message shouldn't be a string
            bytesList = list(bytearray(message, encoding="cp437", errors="ignore"))
            for b in bytesList:
                # with self.lock:
                # print("added byte '%s'" % (bytes([b])))
                self._buffer.put(b)
        except Exception as e:
            print(type(message))
            print("_add_message", e)

    def read(self, size=1):
        """read reads up to size bytes of data, exiting when size bytes have been
        read, or the timeout has been reached"""
        retval = b""
        end = time.time() + self.timeout
        for _ in range(size):
            timeout = end - time.time()
            if timeout < 0:
                break
            try:
                retval = retval + bytes([self._buffer.get(block=True, timeout=timeout)])
            except queue.Empty:
                break
        return retval

    def read_until(self, expected, size=None):
        retval = b""
        if type(expected) == str:
            expected = expected.encode()
        end = time.time() + self.timeout
        if size is None:
            size = sys.maxsize
        for _ in range(size):
            timeout = end - time.time()
            if timeout < 0:
                break
            try:
                retval = retval + bytes([self._buffer.get(block=True, timeout=timeout)])
            except queue.Empty:
                break

            if expected in retval:
                break
        return retval

    def write(self, data):
        """write sends the given bytes to the remote serial port"""
        if self._ws and self._opened:
            # print("ws write", data)
            self._ws.send(data)

    def flush(self):
        """flush ensures that any outstanding bytes are transmitted."""
        pass

    def in_waiting(self):
        """in_waiting returns the number of outstanding bytes yet to be consumed"""
        return self._buffer.qsize()

    def reset_input_buffer(self):
        """reset_input_buffer flushes the input buffer, discarding all its contents"""
        while True:
            try:
                self._buffer.get(False)
            except queue.Empty:
                break

    def reset_output_buffer(self):
        """reset_output_buffer clears the output buffer"""
        pass

    @property
    def baudrate(self):
        state = _get_json(
            self._server,
            self._api_token,
            "/api/v1/{}/config".format(self._name),
        )
        return int(state["baudrate"])

    @baudrate.setter
    def baudrate(self, baudrate):
        print("Setting baudrate: {}".format(baudrate))
        _post_json(
            self._server,
            self._api_token,
            "/api/v1/{}/config".format(self._name),
            {"baudrate": baudrate},
        )

    def readable(self):
        return not self._buffer.empty()

    def writable(self):
        return True

    def seekable(self):
        return False

    @property
    def name(self):
        return self._name


class HardwareAPIRelay:
    def __init__(self, device_name, api_token, relay_name, server="https://hardware-api.com"):
        self.device_name = device_name
        self.api_token = api_token
        self.relay_name = relay_name
        self.server = urlparse(server)

    def set(self, state):
        _post_json(
            self.server,
            self.api_token,
            "/api/v1/{}/relay/{}".format(self.device_name, self.relay_name),
            {"value": state},
        )
        if self.get() != state:
            raise Exception("Relay {} didn't change to {}".format(self.relay_name, state))

    def get(self):
        state = _get_json(
            self.server,
            self.api_token,
            "/api/v1/{}/relay/{}".format(self.device_name, self.relay_name),
        )
        return state["value"]

    def power_cycle(self, delay=0.5):
        self.set(False)
        time.sleep(delay)
        self.set(True)


class HardwareAPISDWire:
    def __init__(self, device_name, api_token, sdwire_name, server="https://hardware-api.com"):
        self.server = urlparse(server)
        self.device_name = device_name
        self.api_token = api_token
        self.sdwire_name = sdwire_name

    def _post_json(self, path, json_struct):
        return _post_json(
            self.server,
            self.api_token,
            "/api/v1/{}/{}".format(self.device_name, path),
            json_struct,
        )

    def _get_json(self, path):
        return _get_json(self.server, self.api_token, "api/v1/{}/{}".format(self.device_name, path))

    def is_attached(self):
        return self.get_partitions()["attached"]

    def get_partitions(self):
        return self._get_json("sdwire/{}/partition".format(self.sdwire_name))

    def attach(self, attach):
        return self._post_json("sdwire/{}".format(self.sdwire_name), {"mount": bool(attach)})

    def ls(self, path="", partition=1):
        if path[0] == "/":
            path = path[1:]
        return self._get_json("sd/{}/{}?partition={}".format(self.sdwire_name, path, partition))

    def get(self, path, local_file=None, partition=1):
        if path[0] == "/":
            path = path[1:]
        if local_file == None:
            local_file = os.path.basename(path)
        full_path = _geturl(self.server) + "/api/v1/{}/sd/{}/{}?partition={}".format(
            self.device_name, self.sdwire_name, path, partition
        )
        params = {"api_token": self.api_token}
        r = requests.get(full_path, params=params)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception("Invalid status code {}".format(r.status_code))
        with open(local_file, "wb") as f:
            f.write(r.content)

    def put(self, path, local_file, partition=1):
        if path[0] == "/":
            path = path[1:]

        if len(path) == 0 or path[-1] == "/":
            remotefile = os.path.basename(local_file)
        else:
            remotefile = os.path.basename(path)
            path = os.path.dirname(path)
        full_path = _geturl(self.server) + "/api/v1/{}/sd/{}/{}?partition={}".format(
            self.device_name, self.sdwire_name, path, partition
        )
        params = {"api_token": self.api_token}
        files = {"uploadfile": (remotefile, open(local_file, "rb"), "application/binary")}
        r = requests.post(full_path, params=params, files=files)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception("Unable to upload file: {}".format(r.status_code))

    def rm(self, path, partition=1):
        if path[0] == "/":
            path = path[1:]
        full_path = _geturl(self.server) + "/api/v1/{}/sd/{}/{}?partition={}".format(
            self.device_name, self.sdwire_name, path, partition
        )
        params = {"api_token": self.api_token}
        r = requests.delete(full_path, params=params)
        if r.status_code < 200 or r.status_code >= 300:
            raise Exception("Invalid status code {}".format(r.status_code))

    def raw_write(self, offset, data):
        # If we're supplied a file object for data, then just read it out
        if isinstance(data, io.IOBase):
            data = data.read()
        length = len(data)
        chunk_length = 10 * 1024 * 1024
        for chunk in range(int(offset), int(offset) + length, chunk_length):
            this_length = min(chunk_length, int(offset) + int(length) - chunk)
            self._post_json(
                "sdwire/{}/raw".format(self.sdwire_name),
                {
                    "offset": chunk,
                    "size": this_length,
                    "data": base64.b64encode(data[chunk : chunk + this_length]).decode("ascii"),
                },
            )

    def raw_read(self, offset, length):
        # TODO: Chunk it up into 1MB blocks, since the server limits us to that
        data = b""
        chunk_length = 10 * 1024 * 1024
        for chunk in range(int(offset), int(offset) + int(length), chunk_length):
            this_length = min(chunk_length, int(offset) + int(length) - chunk)
            response = self._get_json(
                "sdwire/{}/raw?size={}&offset={}".format(self.sdwire_name, this_length, chunk)
            )
            data += base64.b64decode(response["data"])
        return data


if __name__ == "__main__":
    import argparse
    import pprint
    import select
    import sys
    import termios
    import tty

    parser = argparse.ArgumentParser(description="Connect to Hardware API")
    parser.add_argument("--device", required=True, help="Device to connect to")
    parser.add_argument("--api_token", required=True, help="API Token to connect with")
    parser.add_argument("--server", default="https://hardware-api.com", help="Server to connect to")
    args = parser.parse_args()

    d = HardwareAPIDevice(args.device, args.api_token)
    if False:
        r = d.get_relay("0")
        r.set(False)
        print("Relay", r.get())
        time.sleep(1)
        r.set(True)
        print("Relay", r.get())

    # SD Card manipulation
    if True:
        # print("sdwire: ", d.get_sdwire_state())
        sd = d.get_sdwire("0")
        pprint.pprint(sd.get_partitions())
        # d.set_sdwire_attach(True)
        # f = d.list_sdcard_files()
        # print("files: ", f)
        # pprint.pprint(f['files'])
        # d.sdcard_download('config.txt')
        # d.sdcard_delete('config.txt')
        # d.sdcard_upload('/', 'config.txt')
        # d.sdcard_download('config.txt', 'config2.txt')
        # d.sdcard_download('u-boot.bin')
        # d.set_sdwire_attach(False)

    # Interactive serial port
    if False:
        s = d.get_serial("console")
        # Make stdin byte-by-byte
        tty.setcbreak(sys.stdin)

        fd = sys.stdin.fileno()
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~(termios.ECHO | termios.ICANON)  # lflags
        new[6][termios.VMIN] = 0
        new[6][termios.VTIME] = 0
        termios.tcsetattr(fd, termios.TCSANOW, new)

        def isData():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

        while True:
            try:
                d = s.read(100)
                if d:
                    sys.stdout.write(d)
                    sys.stdout.flush()
                if isData():
                    d = sys.stdin.read(100)
                    if d:
                        s.write(d)
            except IOError:
                pass
