import asyncio
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Literal
from urllib.parse import unquote

from client import Client
from database_manager import DatabaseManager

try:
    import websockets
except ModuleNotFoundError:
    print("Module relies on `websockets` package")
    print("Please install by running")
    print()
    print("$ pip install websockets")
    import sys

    sys.exit(1)


WEB_HOSTNAME: Literal["127.0.0.0"] = "127.0.0.0"
WEB_PORT: Literal[8080] = 8080

SOCKET_HOSTNAME: Literal["localhost"] = "localhost"
SOCKET_PORT: Literal[8001] = 8001
connected_websockets = set()


class WebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()

            with open("./pages/index.html", "r") as page:
                index_html = page.read()

            self.wfile.write(bytes(index_html, "utf-8"))
        else:
            file_path = unquote(self.path)
            if file_path.startswith("/assets/"):
                file_path = "." + file_path
                if os.path.isfile(file_path):
                    self.send_response(200)
                    if file_path.endswith(".jpg"):
                        self.send_header("Content-type", "image/jpeg")
                    self.end_headers()
                    with open(file_path, "rb") as file:
                        self.wfile.write(file.read())
                else:
                    self.send_response(404)
                    self.end_headers()

    def do_POST(self):
        if self.path == "/send-coords":
            post_data = self.rfile.read(int(self.headers["Content-Length"]))

            client = Client(post_data)
            client.take_picture()

            # Check if an error occured during camera capture
            if client.img_path != "":
                db_manager.insert_coords(client)
                payload = json.dumps(
                    {
                        "x": client.coordinates.x,
                        "y": client.coordinates.y,
                        "image_path": client.img_path,
                    }
                )
                print("Notifying websocket watchers!")
                asyncio.run(self.notify_sockets(payload))

            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error: Endpoint not found")

    async def notify_sockets(self, payload):
        if connected_websockets:
            await asyncio.wait(
                [asyncio.create_task(ws.send(payload)) for ws in connected_websockets]
            )


def start_web_server():
    global db_manager
    db_manager = DatabaseManager()
    webServer = HTTPServer((WEB_HOSTNAME, WEB_PORT), WebServer)
    print("Server started http://%s:%s" % (WEB_HOSTNAME, WEB_PORT))

    async def start():
        while True:
            await asyncio.get_event_loop().run_in_executor(
                None, webServer.handle_request
            )

    return start()


async def handler(websocket, path):
    if path == "/ws":
        connected_websockets.add(websocket)
        try:
            while True:
                payload = await websocket.recv()
                if payload == "get_serial_data":
                    records = db_manager.get_all()
                    await websocket.send(json.dumps(records))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            if websocket in connected_websockets:
                connected_websockets.remove(websocket)


def start_web_socket():
    return websockets.serve(handler, SOCKET_HOSTNAME, SOCKET_PORT)


async def main():
    webserver = start_web_server()
    websocket = await start_web_socket()

    await asyncio.gather(webserver, websocket.wait_closed())
