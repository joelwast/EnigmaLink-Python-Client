import tkinter as tk
from tkinter import scrolledtext, simpledialog, Menu, messagebox
import socket
import threading
import time

# Función para solicitar la dirección IP y el puerto del servidor
def get_server_info():
    global server_host, server_port, username
    server_host = server_ip_entry.get()
    try:
        server_port = int(server_port_entry.get())
    except ValueError:
        messagebox.showerror("Error", "El puerto debe ser un número entero válido.")
        return

    username = username_entry.get()
    server_info_window.destroy()

# Función para enviar mensajes al servidor
def send_message(event=None):
    message = message_entry.get()
    if message:
        current_time = time.strftime("%H:%M:%S")  # Hora actual
        full_message = f"{current_time} {username}: {message}"
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, full_message + '\n')
        chat_log.config(state=tk.DISABLED)
        try:
            client_socket.send(full_message.encode())
        except Exception as e:
            print(f"Error al enviar mensaje: {str(e)}")
        message_entry.delete(0, tk.END)

# Función para manejar la recepción de mensajes del servidor
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, message + '\n')
            chat_log.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error al recibir mensaje: {str(e)}")
            break

# Configurar la ventana de solicitud de información del servidor
server_info_window = tk.Tk()
server_info_window.title("Configuración del Servidor")

server_ip_label = tk.Label(server_info_window, text="Dirección IP del Servidor:")
server_ip_label.pack()

server_ip_entry = tk.Entry(server_info_window)
server_ip_entry.pack()

server_port_label = tk.Label(server_info_window, text="Puerto del Servidor:")
server_port_label.pack()

server_port_entry = tk.Entry(server_info_window)
server_port_entry.pack()

username_label = tk.Label(server_info_window, text="Nombre de Usuario:")
username_label.pack()

username_entry = tk.Entry(server_info_window)
username_entry.pack()

server_info_button = tk.Button(server_info_window, text="Aceptar", command=get_server_info)
server_info_button.pack()

# Solicitar dirección IP y puerto del servidor
server_host = ""
server_port = 0
username = ""
server_info_window.mainloop()

# Configurar el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((server_host, server_port))
except Exception as e:
    print(f"Error al conectar al servidor: {str(e)}")
    exit(1)

# Configuración de la interfaz gráfica
window = tk.Tk()
window.title("Chat Cliente")
window.geometry("350x525")

# Barra de menú
menu_bar = Menu(window)
window.config(menu=menu_bar)

chat_log = scrolledtext.ScrolledText(window, state=tk.DISABLED, height=20)
chat_log.pack(fill=tk.BOTH, expand=True)

message_entry = tk.Entry(window, justify='left', font=('Helvetica', 12))
message_entry.pack(fill=tk.X, pady=10)

# Placeholder en la caja de texto
message_entry.insert(0, "Escribe aquí...")
message_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, message_entry))
message_entry.bind("<FocusOut>", lambda event: set_placeholder(event, message_entry))
message_entry.config(fg="grey")

# Función para limpiar el placeholder cuando se hace clic en la caja de texto
def clear_placeholder(event, entry_widget):
    if entry_widget.get() == "Escribe aquí...":
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg="black")

# Función para restablecer el placeholder cuando la caja de texto pierde el enfoque y está vacía
def set_placeholder(event, entry_widget):
    if not entry_widget.get():
        entry_widget.insert(0, "Escribe aquí...")
        entry_widget.config(fg="grey")

# Configurar el sistema de geometría para que los elementos se expandan automáticamente
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Iniciar hilo para recibir mensajes del servidor
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

window.bind("<Return>", send_message)  # Enviar mensaje al presionar Enter

window.mainloop()
