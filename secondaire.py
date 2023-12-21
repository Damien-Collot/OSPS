# secondaire.py: Script pour le serveur secondaire qui gère la communication directe avec les clients.

import os
import time
import socket
import multiprocessing

# Configuration des chemins pour les pipes et du port pour la connexion socket
PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"
HOST = '127.0.0.1'
SECONDARY_PORT = 2223

def handle_secondary_server_connection():
    """ Gère les connexions entrantes des clients et échange des données. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, SECONDARY_PORT))
            s.listen()
            print("Serveur secondaire: Écoute des connexions du client sur le port 2223...")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Serveur secondaire: Connecté au client {addr}")

                    while True:
                        data = conn.recv(1024)
                        if not data or data == b"Deconnexion du client..":
                            break
                        print(f"Serveur secondaire a reçu: {data.decode()}")
                        conn.sendall(b"*infos serv secondaire.....*")

                with open(PATH_TO_WDTUBE, "w") as wdtube:
                    # Informer le serveur principal de la déconnexion du client
                    wdtube.write("client_deconnected\n")
                    wdtube.flush()

    except Exception as e:
        print(f"Erreur survenue sur le serveur secondaire: {e}")

def serveur_secondaire(valeur_shared):
    """ Lance le processus de gestion de la connexion socket et traite les données reçues via les pipes. """
    try:
        p_secondary = multiprocessing.Process(target=handle_secondary_server_connection)
        p_secondary.start()

        with open(PATH_TO_DWTUBE, "r") as dwtube, open(PATH_TO_WDTUBE, "w") as wdtube:
            while True:
                chiffre = int(dwtube.readline().strip())

                # Incrémente et envoie le chiffre modifié au serveur principal
                chiffre += 1
                wdtube.write(f"{chiffre}\n")
                wdtube.flush()

                # Incrémente la valeur dans la mémoire partagée
                valeur_shared.value += 5

        p_secondary.join()

    except Exception as e:
        print(f"Erreur lors du lancement du serveur secondaire: {e}")

if __name__ == '__main__':
    print("Ce script doit être exécuté via le serveur principal")
