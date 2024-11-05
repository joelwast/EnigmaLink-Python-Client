import socket
import threading
import time

# Función para enviar mensajes al servidor
def send_message():
    while True:
        message = input("Escribe un mensaje: ")
        if message:
            current_time = time.strftime("%H:%M:%S")  # Hora actual
            full_message = f"{current_time} {username}: {message}"
            try:
                client_socket.send(full_message.encode())
            except Exception as e:
                print(f"Error al enviar mensaje: {str(e)}")

# Función para manejar la recepción de mensajes del servidor
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except Exception as e:
            print(f"Error al recibir mensaje: {str(e)}")
            break

# Solicitar dirección IP, puerto del servidor y nombre de usuario
server_host = input("Ingresa la dirección IP del servidor: ")
server_port = int(input("Ingresa el puerto del servidor: "))
username = input("Ingresa tu nombre de usuario: ")

# Configurar el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((server_host, server_port))
except Exception as e:
    print(f"Error al conectar al servidor: {str(e)}")
    exit(1)

# Iniciar hilos para enviar y recibir mensajes
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_messages)

send_thread.start()
receive_thread.start()
