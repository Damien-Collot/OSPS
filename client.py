# client.py : 
import socket

HOST = '127.0.0.1'
PORT = 2222

def main():
    try:
        while True:
            choice = int(input("Envoyer une requête de type (1) ou (2) ou quitter (3)\n"))
            if choice == 1 or choice == 2:
                communicate_with_servers(choice)
            else:
                break
    except: 
        print("Error occured for client main")

def communicate_with_servers(choice):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"requetetype1" if choice == 1 else b"requetetype2")
            # Réception des informations du serveur secondaire
            port_data = s.recv(1024)
            secondary_port = int(port_data.decode())
            
            chiffre = input("Entrez un chiffre à envoyer au serveur: ")
            s.sendall(chiffre.encode())
            
            # Recevez les résultats du serveur principal
            results = s.recv(1024).decode()
            print(f"Résultats reçus du serveur principal: {results}")

            # Connexion au serveur secondaire
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_secondary:
                s_secondary.connect((HOST, secondary_port))
                # Envoie un message au serveur secondaire après connexion
                print("Envoyez un message au serveur secondaire ('&&' pour quitter): \n")
                while True:
                    message = input("Client> ")
                    if message == "&&": 
                        s_secondary.sendall(b"Deconnexion du client..")    
                        break
                    s_secondary.sendall(message.encode())
                    response = s_secondary.recv(1024)
                    print(f"Serveur secondaire> {response.decode()}")
    except:
        print("Error while client communate with servers")

if __name__ == '__main__':
    main()
