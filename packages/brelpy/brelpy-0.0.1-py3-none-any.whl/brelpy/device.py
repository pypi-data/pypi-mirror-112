from brelpy.socket import BrelSocket


class BrelDevice:
    def __init__(self, mac: str, device_type: str, socket: BrelSocket):
        self.device_type = device_type
        self.mac = mac
        self.socket = socket

    def __repr__(self) -> str:
        return f"<BrelDevice mac={self.mac} device_type={self.device_type}>"

    def status(self):
        return self.socket.send_and_receive(
            dict(
                msgType="ReadDevice",
                mac=self.mac,
                deviceType=self.device_type,
            ),
            provide_token=True,
        )
