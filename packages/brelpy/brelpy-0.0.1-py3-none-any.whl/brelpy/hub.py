from os import getenv
from typing import Any, Dict, Optional, List

from Crypto.Cipher import AES

from brelpy.device import BrelDevice
from brelpy.socket import BrelSocket


class BrelHub:
    def __init__(self, host: str, port: int = 32100, key: Optional[str] = None):
        self.access_token = None
        self.host = host
        self.port = port
        self.key = key or getenv("BREL_KEY", None)
        self.socket: Optional[BrelSocket] = None
        self._data: Optional[Dict[str, Any]] = None

    def __enter__(self) -> "BrelHub":
        self.socket = BrelSocket(host=self.host, port=self.port)
        self._populate()
        if self.key is not None:
            self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.socket.close()
        self.socket = None

    def authenticate(self) -> None:
        self._populate()
        token = self._data["token"]
        self.socket.access_token = self.get_access_token(key=self.key, token=token).upper()

    @property
    def devices(self) -> List[BrelDevice]:

        data = self.socket.send_and_receive({"msgType": "GetDeviceList"})
        return [BrelDevice(mac=dev["mac"], device_type=dev["deviceType"], socket=self.socket) for dev in data["data"]]

    @staticmethod
    def get_access_token(key: str, token: str) -> str:
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        return cipher.encrypt(token.encode("utf-8")).hex().upper()

    def _populate(self) -> None:
        if self._data is None:
            self._data = self.socket.send_and_receive({"msgType": "GetDeviceList"})
