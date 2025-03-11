import socket
from threading import Thread

def handle_client(client_socket):
    """
    Gère la communication avec un agent connecté.
    """
    while True:
        message = client_socket.recv(1024).decode("utf-8")
        if message.lower() == "exit":
            break
        print(f"Agent: {message}")
        response = generate_response(message)
        client_socket.send(response.encode("utf-8"))
        google_tts(response)
    client_socket.close()

def start_server():
    """
    Démarre le serveur pour accepter les connexions des agents.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("Serveur démarré. En attente de connexions...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion acceptée de {addr}")
        Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()