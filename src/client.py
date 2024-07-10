import json
from dataclasses import dataclass

import cv2
import websockets


def on_message(ws, message):
    print(f"Received message: {message}")


def on_error(ws, error):
    print(f"Encountered error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


def on_open(ws):
    print("Connection opened")
    ws.send("Hello, Server!")


async def main():
    async with websockets.connect(
        "ws://localhost:8001",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    ) as ws:

        ws.on_open = on_open
        ws.run_forever()
        # await ws.send("hello")
        # response = await websocket.recv()
        # print(response)
        # asyncio.get_event_loop().run_until_complete(test())
        # cp = ChargePoint('CP_1', ws)
        # await asyncio.gather(cp.start(), cp.send_boot_notification())


@dataclass(frozen=True)
class Coordinates:
    x: float = 0.00
    y: float = 0.00

    @staticmethod
    def from_json(json_str) -> Coordinates:
        return Coordinates(**(json.loads(json_str)))


class Client:
    coordinates: Coordinates

    def __init__(self, json_str: str) -> None:
        self.coordinates = Coordinates.from_json(json_str)

    def take_picture(self) -> None:
        open_camera = cv2.VideoCapture(0)

        if open_camera.isOpened():
            print("Camera is opened and ready to go!")
        else:
            print("Camera is closed! Please open for capture!")
