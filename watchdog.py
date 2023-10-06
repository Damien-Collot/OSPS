import socket
import time
import multiprocessing
from principal import serveur_principal

HOST = '127.0.0.1'
PORT = 65432
CHECK_INTERVAL = 1
RESPONSE_TIMEOUT = 3

def watchdog_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Watchdog: Écoute des connexions...")
        conn, addr = s.accept()
        with conn:
            print(f"Watchdog: Connecté à {addr}")
            while True:
                conn.sendall(b'ping')
                print("Watchdog: Ping envoyé. Attente du Pong...")
                try:
                    data = conn.recv(1024)
                except ConnectionResetError:
                    print("Watchdog: La connexion a été réinitialisée par le serveur principal.")
                    break
                if not data:
                    print("Watchdog: Connexion perdue avec le serveur principal.")
                    break
                elif data == b'pong':
                    print("Watchdog: Pong reçu du serveur principal.")
                else:
                    print(f"Watchdog: Donnée inattendue reçue : {data}")
                time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    while True:
        watchdog_server()

