import socket
import time
import argparse


def udp_client(ip: str, port: int, message: bytes) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message, (ip, port))
        return sock.recv(1024)


def main():
    parser = argparse.ArgumentParser(description='UDP Server Mock.')
    parser.add_argument('server_port', type=int, help='Server port')
    parser.add_argument('msg', type=str, help='Message')
    parser.add_argument('--server_ip', type=str, help='Server ip')

    args = parser.parse_args()

    msg = bytes(args.msg, 'ascii')

    print(f'[{time.time()}] Outgoing: {msg}')

    reply = udp_client(args.server_ip or '127.0.0.1', args.server_port, msg)

    print(f'[{time.time()}] Incoming: {reply}')


if __name__ == "__main__":
    main()
