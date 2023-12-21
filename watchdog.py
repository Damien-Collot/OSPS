import socket
import time
import multiprocessing
from principal import startServer

HOST = '127.0.0.1'
PORT = 65432
CHECK_INTERVAL = 1
RESPONSE_TIMEOUT = 3

def watchdog_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Watchdog: Écoute des connexions...")
        multiprocessing.Process(target=startServer).start()
        conn, addr = s.accept()
        with conn:
            print(f"Watchdog: Connecté à {addr}")
            while True:
                conn.sendall(b'ping')
                try:
                    data = conn.recv(1024)
                except ConnectionResetError:
                    multiprocessing.Process(target=startServer).start()
                    break
                if not data:
                    multiprocessing.Process(target=startServer).start()
                    break
                time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    while True:
        watchdog_server()

