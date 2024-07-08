from threading import Thread

import server.socket as hv_websocket
import server.web as hv_web


def start_web_server():
    hv_web.run()


def start_websocket_server():
    hv_websocket.run()


if __name__ == "__main__":
    thread = Thread(target=start_websocket_server())
    thread.start()
    start_websocket_server()
