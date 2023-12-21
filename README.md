# OSPS
# README pour le Projet Python de Communication Réseau

## Description du Projet

Ce projet est un système de communication réseau en Python comprenant un client, un serveur principal, un serveur secondaire, et un processus de surveillance (watchdog). Le système permet une interaction bidirectionnelle entre le client et les serveurs, avec des mécanismes de communication avancés tels que les tubes nommés et la mémoire partagée. Le watchdog surveille le serveur principal et garantit sa disponibilité continue.

## Composants

### Client (client.py):
Interagit avec les serveurs principal et secondaire.
Envoie des requêtes et reçoit des réponses.
### Serveur Principal (principal.py):
Traite les requêtes du client.
Communique avec le serveur secondaire via des tubes nommés et de la mémoire partagée.
### Serveur Secondaire (secondaire.py):
Reçoit des données du serveur principal.
Permet la communication directe avec le client.
### Watchdog (watchdog.py):
Surveille et maintient le serveur principal.
Redémarre le serveur principal en cas de défaillance.

## Installation

Aucune dépendance externe spécifique n'est requise pour ce projet, à l'exception de Python 3. Assurez-vous que Python 3 est installé sur votre système.

## Utilisation

### Démarrage du Serveur Principal et du Watchdog :
Exécutez watchdog.py pour démarrer le watchdog, le serveur principal et le serveur secondaire.
### Démarrage du Client :
Exécutez client.py pour commencer à interagir avec les serveurs.

## Notes Importantes

Assurez-vous que les ports utilisés par les serveurs ne sont pas bloqués ou déjà utilisés sur votre système.
Le système utilise des adresses IP locales pour la communication, donc il est conçu pour fonctionner sur un réseau local.
