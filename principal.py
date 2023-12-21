# principal.py: Script pour le serveur principal gérant les connexions client et la communication avec le serveur secondaire.

import os
import time
import socket
import multiprocessing
from secondaire import serveur_secondaire

# Configuration des adresses et ports
HOST = '127.0.0.1'
PORT = 65432
PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"
NUM_EXCHANGES = 2
CLIENT_PORT = 2222
SECONDARY_PORT = 2223

# Création de tubes nommés (pipes) si non existants
if not os.path.exists(PATH_TO_DWTUBE):
    os.mkfifo(PATH_TO_DWTUBE)

if not os.path.exists(PATH_TO_WDTUBE):
    os.mkfifo(PATH_TO_WDTUBE)


def connect_to_watchdog():
    """ Maintient une connexion avec le service watchdog. """
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
    """ Gère le serveur principal, accepte les connexions client et communique avec le serveur secondaire. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, CLIENT_PORT))
            server_socket.listen()
            print("Serveur principal en attente d'une connexion client...")

            while True:
                client_conn, client_addr = server_socket.accept()
                with client_conn:
                    print(f"Client connecté depuis {client_addr}")
                    request_type = client_conn.recv(1024).decode()

                    if request_type in ["requetetype1", "requetetype2"]:
                        client_conn.sendall(str(SECONDARY_PORT).encode())
                    else:
                        print(f"Requête non reconnue: {request_type}")
                        client_conn.close()
                        continue

                    # Communication avec le serveur secondaire
                    with open(PATH_TO_DWTUBE, "w") as dwtube, open(PATH_TO_WDTUBE, "r") as wdtube:
                        chiffre = int(client_conn.recv(1024).decode())
                        dwtube.write(f"{chiffre}\n")
                        dwtube.flush()

                        valeur_shared.value = chiffre

                        chiffre_mis_a_jour_pipe = int(wdtube.readline().strip())
                        chiffre_mis_a_jour_shared_memory = valeur_shared.value

                        client_conn.sendall(
                            f"Pipe: {chiffre_mis_a_jour_pipe}, Shared Memory: {chiffre_mis_a_jour_shared_memory}".encode())

                        # Attente de la confirmation de déconnexion du client du serveur secondaire
                        while True:
                            confirmation = wdtube.readline().strip()
                            if confirmation == "client_deconnected":
                                print("Le client s'est déconnecté du serveur secondaire.")
                                break

        if os.path.exists(PATH_TO_DWTUBE):
            os.remove(PATH_TO_DWTUBE)

        if os.path.exists(PATH_TO_WDTUBE):
            os.remove(PATH_TO_WDTUBE)
    except Exception as e:
        print(f"Erreur survenue dans le serveur principal: {e}")


def startServer():
    """ Fonction pour démarrer le serveur lorsqu'il est exécuté comme script principal. """
    print("Ce script doit être exécuté via le watchdog")


if __name__ == '__main__':
    startServer()
