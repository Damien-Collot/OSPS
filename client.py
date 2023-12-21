# client.py: Script pour le client se connectant au serveur principal et secondaire.

import socket

HOST = '127.0.0.1'  # Adresse hôte du serveur
PORT = 2222  # Port pour la connexion initiale au serveur principal

def main():
    """ Point d'entrée principal du client. """
    try:
        while True:
            # Demande à l'utilisateur le type de requête à envoyer
            choice = int(input("Envoyer une requête de type (1) ou (2) ou quitter (3)\n"))
            if choice == 1 or choice == 2:
                communicate_with_servers(choice)
            else:
                break
    except Exception as e:
        print(f"Erreur survenue dans le client principal: {e}")

def communicate_with_servers(choice):
    """ Gère la communication entre le client et les serveurs. """
    try:
        # Connexion au serveur principal
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # Envoi de la requête au serveur principal
            s.sendall(b"requetetype1" if choice == 1 else b"requetetype2")

            # Réception des informations du serveur secondaire
            port_data = s.recv(1024)
            secondary_port = int(port_data.decode())

            # Envoi d'un chiffre au serveur principal
            chiffre = input("Entrez un chiffre à envoyer au serveur: ")
            s.sendall(chiffre.encode())

            # Réception des résultats du serveur principal
            results = s.recv(1024).decode()
            print(f"Résultats reçus du serveur principal: {results}")

            # Connexion et communication avec le serveur secondaire
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_secondary:
                s_secondary.connect((HOST, secondary_port))
                print("Envoyez un message au serveur secondaire ('&&' pour quitter): \n")
                while True:
                    message = input("Client> ")
                    if message == "&&":
                        s_secondary.sendall(b"Deconnexion du client..")
                        break
                    s_secondary.sendall(message.encode())
                    response = s_secondary.recv(1024)
                    print(f"Serveur secondaire> {response.decode()}")
    except Exception as e:
        print(f"Erreur lors de la communication du client avec les serveurs: {e}")

if __name__ == '__main__':
    main()
