import signal
import time
import os
import multiprocessing
from principal import serveur_principal

CHECK_INTERVAL = 5  # Vérifie chaque 5 secondes
RESPONSE_TIMEOUT = 3  # Attends 3 secondes pour une réponse
process_to_check = None

def send_check_signal(signum, frame):
    global process_to_check
    if process_to_check:
        os.kill(process_to_check.pid, signal.SIGUSR1)

def receive_response_signal(signum, frame):
    global got_response
    got_response = True

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, send_check_signal)
    signal.signal(signal.SIGUSR2, receive_response_signal)

    # Démarrer le serveur principal
    valeur_shared = multiprocessing.Value('i', 0)
    process_to_check = serveur_principal(valeur_shared)

    while True:
        got_response = False
        signal.alarm(CHECK_INTERVAL)
        time.sleep(RESPONSE_TIMEOUT)

        if not got_response:
            print("Watchdog: Pas de réponse, redémarrage du serveur")
            os.kill(process_to_check.pid, signal.SIGKILL)
            process_to_check = serveur_principal(valeur_shared)
