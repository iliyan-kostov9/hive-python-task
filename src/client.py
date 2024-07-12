import json
import uuid
from dataclasses import dataclass

import cv2


@dataclass(frozen=True)
class Coordinates:
    x: float = 0.00
    y: float = 0.00

    @staticmethod
    def from_json(json_str):
        return Coordinates(**(json.loads(json_str)))


class Client:
    coordinates: Coordinates
    img_path: str

    def __init__(self, json_str: str) -> None:
        self.coordinates = Coordinates.from_json(json_str)
        self.img_path = ""

    def take_picture(self) -> None:
        open_camera = cv2.VideoCapture(0)

        if open_camera.isOpened():
            print("Camera is opened and ready to go!")

            ret, frame = open_camera.read()
            self.img_path = f"assets/{str(uuid.uuid4())}_img.jpg"

            cv2.imwrite(self.img_path, frame)
            print("Image saved!")

            open_camera.release()
            cv2.destroyAllWindows()
        else:
            print("Camera is closed! Please open for capture!")
