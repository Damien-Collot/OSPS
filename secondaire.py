import os
import time
import signal

PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"

def handle_check_signal(signum, frame):
    # Envoie une réponse au watchdog
    os.kill(os.getppid(), signal.SIGUSR2)

def serveur_secondaire(valeur_shared):
    with open(PATH_TO_DWTUBE, "r") as dwtube, open(PATH_TO_WDTUBE, "w") as wdtube:
        while True:
            message = dwtube.readline().strip()
            
            print(f"Serveur secondaire (Mémoire partagée): valeur lue {valeur_shared.value}")

            if not message:
                break
            
            print(f"Serveur secondaire: Reçu '{message}'")
            
            print("Serveur secondaire: Envoi de 'pong'")
            wdtube.write("pong\n")
            wdtube.flush()

            time.sleep(1)

if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, handle_check_signal)
    print("Ce script doit être exécuté via le serveur principal")
