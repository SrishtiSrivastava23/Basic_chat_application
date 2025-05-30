import socket
import threading
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# Encryption key (same as server)
encryption_key = b'p5LaSWj7xDXBABt9DijLGffsIBzJb63rBjpzuzCpkwU='
cipher = Fernet(encryption_key)

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("400x500")

        self.nickname = self.ask_nickname()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 9999))
        self.client.send(self.nickname.encode())

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', bg="#F0F0F0", fg="#333", font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.entry.bind("<Return>", self.send_message)

        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def ask_nickname(self):
        nickname = simpledialog.askstring("Nickname", "Choose a nickname:")
        return nickname if nickname else "Anonymous"

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            formatted_message = f"{self.nickname}: {message}"
            encrypted_message = cipher.encrypt(formatted_message.encode())
            self.client.send(encrypted_message)
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = cipher.decrypt(encrypted_message).decode()
                self.display_message(decrypted_message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client_app = ChatClient(root)
    root.mainloop()
