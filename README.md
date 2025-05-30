# Basic_chat_application

# Encrypted Python Chat Application

A simple encrypted chat application built with Python using sockets, threading, and Fernet symmetric encryption. The project includes a server that handles multiple clients, and a client with a Tkinter GUI to send and receive encrypted messages in real-time.

## Features

* Encrypted communication using Fernet symmetric encryption (AES-based)
* Multi-client support via threading on the server
* Tkinter-based GUI client for easy chatting
* Real-time message broadcast to all connected clients
* Simple nickname-based user identification

## Prerequisites

* Python 3.6+
* Required packages:

  * `cryptography`
  * `tkinter` (usually included with Python)

Install dependencies with:

bash
pip install cryptography


## How to Run

First, generate the encryption key:

bash
python generate_key.py


Then, start the server:

bash
python server.py


Finally, start one or more clients (each in a separate terminal window):

bash
python client.py

## How It Works

* The server listens for incoming connections from clients.
* Clients send their chosen nickname upon connecting.
* All messages are encrypted with the shared key before being sent.
* The server broadcasts encrypted messages to all connected clients.
* Clients decrypt incoming messages and display them in the chat window.

## Project Structure

Basic_chat/
│
├── server.py          # Server application
├── client.py          # Client application with Tkinter GUI
├── generate_key.py    # Script to generate encryption key
├── secret.key         # Encryption key file
└── README.md          # Project documentation


