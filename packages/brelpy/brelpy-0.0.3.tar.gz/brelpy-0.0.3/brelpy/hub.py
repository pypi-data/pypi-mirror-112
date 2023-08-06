from os import getenv
from typing import Any, Dict, Optional, List

from Crypto.Cipher import AES

from brelpy.device import BrelDevice
from brelpy.exceptions import NoKeyException, NotConnectedException
from brelpy.socket import BrelSocket


class BrelHub:
    def __init__(self, host: str, port: int = 32100, key: Optional[str] = None):
        self.access_token = None
        self.host = host
        self.port = port
        self.key = key or getenv("BREL_KEY", None)
        self.socket: Optional[BrelSocket] = None
        self._data: Optional[Dict[str, Any]] = None
        self._devices: Optional[List[BrelDevice]] = None

    def __enter__(self) -> "BrelHub":
        self.socket = BrelSocket(host=self.host, port=self.port)
        self._populate()
        self._authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.socket.close()
        self.socket = None

    @property
    def devices(self) -> List[BrelDevice]:
        if self._data is None:
            raise NotConnectedException("Hub is not connected.")
        if self._devices is None:
            self._devices = [
                BrelDevice(mac=dev["mac"], device_type=dev["deviceType"], socket=self.socket)
                for dev in self._data["data"]
                if dev["deviceType"] != "02000001"
            ]
        return self._devices

    @property
    def mac(self) -> str:
        if self._data is None:
            raise NotConnectedException("Hub is not connected.")
        for dev in self._data["data"]:
            if dev["deviceType"] == "02000001":
                return dev["mac"]
        raise Exception("Hub is missing from device list.")

    def _authenticate(self) -> None:
        if self.key is None:
            raise NoKeyException("No key was provided.")
        token = self._data["token"]
        self.socket.access_token = self._get_access_token(key=self.key, token=token).upper()

    @staticmethod
    def _get_access_token(key: str, token: str) -> str:
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        return cipher.encrypt(token.encode("utf-8")).hex().upper()

    def _populate(self) -> None:
        if self._data is None:
            self._data = self.socket.send_and_receive({"msgType": "GetDeviceList"})
