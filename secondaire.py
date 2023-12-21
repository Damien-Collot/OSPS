import os
import time
import socket
import multiprocessing

PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"
HOST = '127.0.0.1'
SECONDARY_PORT = 2223

def handle_secondary_server_connection():
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
                    wdtube.write("client_deconnected\n")
                    wdtube.flush()
    except:
        print("Secondary server error while receiveing messages")


def serveur_secondaire(valeur_shared):
    try:
        p_secondary = multiprocessing.Process(target=handle_secondary_server_connection)
        p_secondary.start()
        with open(PATH_TO_DWTUBE, "r") as dwtube, open(PATH_TO_WDTUBE, "w") as wdtube:
            while True:
                # Lit le chiffre du serveur principal via le pipe
                chiffre = int(dwtube.readline().strip())
                
                # Incrémente le chiffre pour le pipe et l'écrit dans le pipe
                chiffre += 1
                wdtube.write(f"{chiffre}\n")
                wdtube.flush()
                
                # Incrémente le chiffre pour la mémoire partagée  
                valeur_shared.value += 5
        p_secondary.join()
    except:
        print("Error launching secondary server")

if __name__ == '__main__':
    print("Ce script doit être exécuté via le serveur principal")
