import os
import time
import multiprocessing
import signal
from secondaire import serveur_secondaire

PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"
NUM_EXCHANGES = 10

if not os.path.exists(PATH_TO_DWTUBE):
    os.mkfifo(PATH_TO_DWTUBE)

if not os.path.exists(PATH_TO_WDTUBE):
    os.mkfifo(PATH_TO_WDTUBE)

def handle_check_signal(signum, frame):
    # Envoie une réponse au watchdog
    os.kill(os.getppid(), signal.SIGUSR2)

def serveur_principal(valeur_shared):
    with open(PATH_TO_DWTUBE, "w") as dwtube, open(PATH_TO_WDTUBE, "r") as wdtube:
        for _ in range(NUM_EXCHANGES):
            valeur_shared.value += 1
            print(f"Serveur principal (Mémoire partagée): valeur mise à jour à {valeur_shared.value}")

            print("Serveur principal: Envoi de 'ping'")
            dwtube.write("ping\n")
            dwtube.flush()

            # Attendre une réponse
            response = wdtube.readline().strip()
            print(f"Serveur principal: Reçu '{response}'")

            time.sleep(1)

    os.remove(PATH_TO_DWTUBE)
    os.remove(PATH_TO_WDTUBE)

if __name__ == '__main__':
    valeur_shared = multiprocessing.Value('i', 0)
    signal.signal(signal.SIGUSR1, handle_check_signal)

    # Lancement du serveur secondaire avec fork
    p = multiprocessing.Process(target=serveur_secondaire, args=(valeur_shared,))
    p.start()

    serveur_principal(valeur_shared)

    p.join()
