from brelpy.socket import BrelSocket
from brelpy.types import Message
from typing import Any, Dict


class BrelDevice:
    def __init__(self, mac: str, device_type: str, socket: BrelSocket):
        self.device_type = device_type
        self.mac = mac
        self.socket = socket
        self._status: Dict[str, int] = {}
        self._read_device()

    def __repr__(self) -> str:
        return f"<BrelDevice mac={self.mac} device_type={self.device_type}>"

    def _get_status(self, data: Message) -> None:
        if data["msgType"] in ("ReadDeviceAck", "WriteDeviceAck"):
            self._status = data["data"]

    @property
    def battery_level(self) -> int:
        level = self._status["batteryLevel"]
        return round((min(max(level, 1160), 1240) - 1160) / 80 * 100)

    @property
    def battery_voltage(self) -> float:
        return self._status["batteryLevel"] / 100

    def close(self) -> None:
        self._write_device(dict(operation=0))

    def down(self) -> None:
        self.close()

    def open(self) -> None:
        self._write_device(dict(operation=1))

    @property
    def operation(self) -> int:
        return self._status["operation"]

    @property
    def position(self) -> int:
        return self._status["currentPosition"]

    @position.setter
    def position(self, value: int) -> None:
        self._write_device(dict(targetPosition=value))

    def stop(self) -> None:
        self._write_device(dict(operation=2))

    def up(self) -> None:
        self.open()

    def update(self) -> None:
        self._write_device(data=dict(operation=5))

    def _read_device(self) -> Dict[str, Any]:
        result = self.socket.send_and_receive(
            dict(
                msgType="ReadDevice",
                mac=self.mac,
                deviceType=self.device_type,
            ),
            provide_token=True,
        )
        self._get_status(result)
        return result

    def _write_device(self, data: Dict[str, int]) -> Dict[str, Any]:
        result = self.socket.send_and_receive(
            dict(msgType="WriteDevice", mac=self.mac, deviceType=self.device_type, data=data), provide_token=True
        )
        self._get_status(result)
        return result
