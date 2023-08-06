from typing import Any, Dict

from brelpy.socket import BrelSocket
from brelpy.types import BlindsType, Message, LimitState, Operation, VoltageMode, WirelessMode


class BrelDevice:
    def __init__(self, mac: str, device_type: str, socket: BrelSocket):
        self._device_type = device_type
        self.mac = mac
        self.socket = socket
        self._status: Dict[str, int] = {}
        self._read_device()

    def __repr__(self) -> str:
        return f"<BrelDevice mac={self.mac} device_type={self._device_type}>"

    @property
    def angle(self) -> int:
        return self._status["currentAngle"]

    @angle.setter
    def angle(self, value: int) -> None:
        self._write_device(dict(targetAngle=value))

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

    @property
    def is_moving(self) -> bool:
        return self.operation in (Operation.OPENING, Operation.CLOSING)

    @property
    def limit_state(self) -> LimitState:
        return LimitState(self._status["currentState"])

    def open(self) -> None:
        self._write_device(dict(operation=1))

    @property
    def operation(self) -> Operation:
        return Operation(self._status["operation"])

    @property
    def position(self) -> int:
        return self._status["currentPosition"]

    @position.setter
    def position(self, value: int) -> None:
        self._write_device(dict(targetPosition=value))

    @property
    def rssi(self) -> int:
        return self._status["RSSI"]

    def stop(self) -> None:
        self._write_device(dict(operation=2))

    @property
    def type(self) -> BlindsType:
        return BlindsType(self._status["type"])

    def up(self) -> None:
        self.open()

    def update(self) -> None:
        self._write_device(data=dict(operation=5))

    @property
    def voltage_mode(self) -> VoltageMode:
        return VoltageMode(self._status["voltageMode"])

    @property
    def wireless_mode(self) -> WirelessMode:
        return WirelessMode(self._status["wirelessMode"])

    def _get_status(self, data: Message) -> None:
        if data["mac"] == self.mac and data["msgType"] in ("ReadDeviceAck", "WriteDeviceAck"):
            self._status = data["data"]

    def _read_device(self) -> Dict[str, Any]:
        result = self.socket.send_and_receive(
            dict(
                msgType="ReadDevice",
                mac=self.mac,
                deviceType=self._device_type,
            ),
            provide_token=True,
        )
        self._get_status(result)
        return result

    def _write_device(self, data: Dict[str, int]) -> Dict[str, Any]:
        result = self.socket.send_and_receive(
            dict(msgType="WriteDevice", mac=self.mac, deviceType=self._device_type, data=data), provide_token=True
        )
        self._get_status(result)
        return result
