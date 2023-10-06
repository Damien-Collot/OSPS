import os
import time
import socket
import multiprocessing
from secondaire import serveur_secondaire

HOST = '127.0.0.1'
PORT = 65432
PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"
NUM_EXCHANGES = 10

if not os.path.exists(PATH_TO_DWTUBE):
    os.mkfifo(PATH_TO_DWTUBE)

if not os.path.exists(PATH_TO_WDTUBE):
    os.mkfifo(PATH_TO_WDTUBE)

def connect_to_watchdog():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                data = s.recv(1024)
                if not data:
                    break
                if data == b'ping':
                    s.sendall(b'pong')
            except ConnectionResetError:
                print("La connexion avec le watchdog a été interrompue.")
                break


def serveur_principal(valeur_shared):
    p_watchdog = multiprocessing.Process(target=connect_to_watchdog)
    p_watchdog.start()

    with open(PATH_TO_DWTUBE, "w") as dwtube, open(PATH_TO_WDTUBE, "r") as wdtube:
        for _ in range(NUM_EXCHANGES):
            valeur_shared.value += 1
            print(f"Serveur principal (Mémoire partagée): valeur mise à jour à {valeur_shared.value}")

            print("Serveur principal: Envoi de 'ping'")
            dwtube.write("ping\n")
            dwtube.flush()
            print("Serveur principal: 'ping' envoyé.")

            print("Serveur principal: Attente de la réponse ...")
            response = wdtube.readline().strip()
            print(f"Serveur principal: Reçu '{response}'")

            time.sleep(1)

    if os.path.exists(PATH_TO_DWTUBE):
        os.remove(PATH_TO_DWTUBE)

    if os.path.exists(PATH_TO_WDTUBE):
        os.remove(PATH_TO_WDTUBE)

    p_watchdog.terminate()
    p_watchdog.join()



if __name__ == '__main__':
    valeur_shared = multiprocessing.Value('i', 0)

    # Lancement du serveur secondaire avec fork
    p = multiprocessing.Process(target=serveur_secondaire, args=(valeur_shared,))
    p.start()

    serveur_principal(valeur_shared)

    p.join()
