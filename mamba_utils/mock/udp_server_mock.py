import threading
import socketserver
import argparse
import time


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        print(f'[{time.time()}] Incoming: {data}')

        reply = data.upper()

        print(f'[{time.time()}] Outgoing: {reply}')

        socket.sendto(reply, self.client_address)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class UdpServerMock:
    def __init__(self, host, port):
        self._server = ThreadedUDPServer((host, port),
                                         ThreadedUDPRequestHandler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self._server_thread = threading.Thread(
            target=self._server.serve_forever)
        # Exit the server thread when the main thread terminates
        self._server_thread.daemon = True
        self._server_thread.start()

    def shutdown(self):
        self._server.shutdown()
        self._server_thread.join()


def main():
    parser = argparse.ArgumentParser(description='UDP Server Mock.')
    parser.add_argument('host_port', type=int, help='Host port')
    parser.add_argument('--host_ip', type=str, help='Host ip')

    args = parser.parse_args()

    UdpServerMock(args.host_ip or '127.0.0.1', args.host_port)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Mamba UDP Server Mock Finalized')
            break


if __name__ == "__main__":
    main()
