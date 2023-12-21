import os
import time
import socket
import multiprocessing
from secondaire import serveur_secondaire

HOST = '127.0.0.1'
PORT = 65432
PATH_TO_DWTUBE = "dwtube1"
PATH_TO_WDTUBE = "wdtube1"
NUM_EXCHANGES = 2
CLIENT_PORT = 2222
SECONDARY_PORT = 2223

if not os.path.exists(PATH_TO_DWTUBE):
    os.mkfifo(PATH_TO_DWTUBE)

if not os.path.exists(PATH_TO_WDTUBE):
    os.mkfifo(PATH_TO_WDTUBE)

def connect_to_watchdog():
    print('PArle watchdog')
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
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, 2222))
            server_socket.listen()
            print("Serveur principal en attente d'une connexion client...")
            while True:
                client_conn, client_addr = server_socket.accept()
                with client_conn:
                    print(f"Client connecté depuis {client_addr}")
                    request_type = client_conn.recv(1024).decode()
                    if request_type == "requetetype1" or request_type == "requetetype2":
                        # Informer le client du port du serveur secondaire.
                        client_conn.sendall(str(SECONDARY_PORT).encode())
                    else:
                        print(f"Requête non reconnue: {request_type}")
                        client_conn.close()
                        continue


                    # Communication avec le serveur secondaire une fois que le client est connecté
                    with open(PATH_TO_DWTUBE, "w") as dwtube, open(PATH_TO_WDTUBE, "r") as wdtube:
                        # Reçoit le chiffre du client
                        chiffre = int(client_conn.recv(1024).decode())
                        
                        # Envoit le chiffre au serveur secondaire via le pipe
                        print(f"Envoi du chiffre/nombre {chiffre} par le pipe.\n")
                        dwtube.write(f"{chiffre}\n")
                        dwtube.flush()

                        # Envoit le chiffre au serveur secondaire via la mémoire partagée
                        print(f"Envoi du chiffre/nombre {chiffre} par la mémoire partagée.\n")
                        valeur_shared.value = chiffre
                        
                        # Reçoit le chiffre mis à jour du serveur secondaire via le pipe
                        chiffre_mis_a_jour_pipe = int(wdtube.readline().strip())
                        print(f"Chiffre/nombre {chiffre_mis_a_jour_pipe} reçu par le pipe.\n")
                        
                        # Utilise la valeur mise à jour de la mémoire partagée
                        chiffre_mis_a_jour_shared_memory = valeur_shared.value
                        print(f"Chiffre/nombre {chiffre_mis_a_jour_shared_memory} reçu par la mémoire partagée.\n")
                        
                        # Envoie les résultats au client
                        client_conn.sendall(f"Pipe: {chiffre_mis_a_jour_pipe}, Shared Memory: {chiffre_mis_a_jour_shared_memory}".encode())
                        
                        while True:
                            confirmation = wdtube.readline().strip()
                            if confirmation == "client_deconnected":
                                print("Le client s'est déconnecté du serveur secondaire.")
                                break

        if os.path.exists(PATH_TO_DWTUBE):
            os.remove(PATH_TO_DWTUBE)

        if os.path.exists(PATH_TO_WDTUBE):
            os.remove(PATH_TO_WDTUBE)
    except:
        print("Error with principal server")


def startServer():
    p = multiprocessing.Process(target=connect_to_watchdog)

    valeur_shared = multiprocessing.Value('i', 0)

    # Lancement du serveur secondaire avec fork
    multiprocessing.Process(target=serveur_secondaire, args=(valeur_shared,)).start()
    p.start()

    serveur_principal(valeur_shared)

    p.join()

