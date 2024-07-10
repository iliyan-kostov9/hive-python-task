import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Literal

from client import Client

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

global client


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("./pages/index.html", "r") as page:
                index_html = page.read()

            self.wfile.write(bytes(index_html, "utf-8"))

    def do_POST(self):
        if self.path == "/send-coords":
            post_data = self.rfile.read(int(self.headers["Content-Length"]))
            coords = json.loads(post_data)

            client = Client(coords)
            client.take_picture()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error: Endpoint not found")


def start_web_server():
    webServer = HTTPServer((WEB_HOSTNAME, WEB_PORT), WebServer)
    print("Server started http://%s:%s" % (WEB_HOSTNAME, WEB_PORT))

    async def start():
        while True:
            await asyncio.get_event_loop().run_in_executor(
                None, webServer.handle_request
            )

    return start()


async def handler(websocket: Any):
    while True:
        async for message in websocket:
            print(message)
            event = {}
            await websocket.send(json.dumps(event))


def start_web_socket():
    return websockets.serve(handler, SOCKET_HOSTNAME, SOCKET_PORT)


async def main():
    webserver = start_web_server()
    websocket = await start_web_socket()

    await asyncio.gather(webserver, websocket.wait_closed())
