import socket
import time
import multiprocessing
from principal import startServer

# Configuration du serveur watchdog
HOST = '127.0.0.1'
PORT = 65432
CHECK_INTERVAL = 1  # Intervalle pour envoyer des pings au serveur principal
RESPONSE_TIMEOUT = 3  # Délai avant de considérer que le serveur principal ne répond pas

def watchdog_server():
    """ Fonction principale du serveur watchdog pour surveiller le serveur principal. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Préparation du socket pour écouter les connexions
        s.bind((HOST, PORT))
        s.listen()
        print("Watchdog: Écoute des connexions...")

        # Lancement du serveur principal dans un processus séparé
        multiprocessing.Process(target=startServer).start()

        # Accepte la connexion du serveur principal
        conn, addr = s.accept()
        with conn:
            print(f"Watchdog: Connecté à {addr}")

            # Boucle de surveillance du serveur principal
            while True:
                # Envoi d'un ping au serveur principal
                conn.sendall(b'ping')
                try:
                    data = conn.recv(1024)
                except ConnectionResetError:
                    # Si la connexion est réinitialisée, redémarre le serveur principal
                    multiprocessing.Process(target=startServer).start()
                    break

                if not data:
                    # Si aucune donnée n'est reçue, redémarre également le serveur principal
                    multiprocessing.Process(target=startServer).start()
                    break

                # Attendre avant le prochain ping
                time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    while True:
        # Exécute le serveur watchdog continuellement
        watchdog_server()
