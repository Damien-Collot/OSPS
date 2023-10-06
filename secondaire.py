import os
import time

PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"

def serveur_secondaire(valeur_shared):
    with open(PATH_TO_DWTUBE, "r") as dwtube, open(PATH_TO_WDTUBE, "w") as wdtube:
        while True:
            message = dwtube.readline().strip()

            if not message:
                print("Serveur secondaire: Message vide reçu. Interruption.")
                break

            print(f"Serveur secondaire (Mémoire partagée): valeur lue {valeur_shared.value}")
            print(f"Serveur secondaire: Reçu '{message}'")

            print("Serveur secondaire: Envoi de 'pong'")
            wdtube.write("pong\n")
            wdtube.flush()
            print("Serveur secondaire: 'pong' envoyé.")

            time.sleep(1)

if __name__ == '__main__':
    print("Ce script doit être exécuté via le serveur principal")
