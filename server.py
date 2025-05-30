import socket #socket for networking,
from cryptography.fernet import Fernet #cryptography.fernet for encryption,
import threading #threading to handle multiple tasks concurrently.

# Use the same encryption key for all clients
encryption_key = b'p5LaSWj7xDXBABt9DijLGffsIBzJb63rBjpzuzCpkwU='
cipher = Fernet(encryption_key) #An encryption key is defined and a Fernet cipher object is created for encrypting and decrypting messages.


# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9999))
server.listen()

clients = []
nicknames = []

def broadcast(message): #Defines a function to broadcast messages to all connected clients.
    for client in clients:
        client.send(message)

def handle_client(client_socket):
    print("Client connected.")
    nickname = client_socket.recv(1024).decode()  # Receive the nickname
    nicknames.append(nickname)
    clients.append(client_socket)
    print(f'Nickname of the client is {nickname}!')

    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            
            # Decrypt the message
            decrypted_message = cipher.decrypt(encrypted_message).decode()
            print(decrypted_message)  # Print the message on the server

            # Broadcast the message to other clients
            broadcast(encrypted_message)  # Send the encrypted message

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    clients.remove(client_socket)
    nicknames.remove(nickname)
    print(f"{nickname} has disconnected.") #Closes the client socket and removes the client from the list

# Listen for clients
print("Server listening on port 9999...")
while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
