from datetime import datetime
from json import dumps, loads
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Any, Dict, Optional


class BrelSocket:
    def __init__(self, host: str, port: int):
        self.access_token: Optional[str] = None
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(10)

    def close(self) -> None:
        self.socket.close()

    def __del__(self) -> None:
        self.close()

    def receive(self) -> Dict[str, Any]:
        response, _ = self.socket.recvfrom(1024)
        result = loads(response.decode("utf-8"))
        if result.get("actionResult") == "AccessToken error":
            raise Exception
        return result

    def send(self, data: Dict[str, Any], provide_token: bool = False) -> None:
        data["msgID"] = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        if provide_token:
            if self.access_token is None:
                raise Exception
            data["AccessToken"] = self.access_token
        message = dumps(data).encode("utf-8")
        self.socket.sendto(message, (self.host, self.port))

    def send_and_receive(
        self, data: Dict[str, Any], provide_token: bool = False
    ) -> Dict[str, Any]:
        message_type = data["msgType"]
        self.send(data, provide_token=provide_token)
        return self.wait_for(f"{message_type}Ack")

    def wait_for(self, message_type: str) -> Dict[str, Any]:
        message = {}
        while message.get("msgType") != message_type:
            message = self.receive()
        return message
