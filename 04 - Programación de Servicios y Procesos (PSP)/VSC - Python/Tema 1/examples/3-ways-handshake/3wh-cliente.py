import socket

"""
3-ways-handshake
CÓDIGO DEL CLIENTE

"""

# Crear un socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect(('localhost', 12345))

# Enviar datos al servidor
client_socket.sendall("¡Hola, servidor!".encode())

# Recibir una respuesta del servidor
data = client_socket.recv(1024)
print(f"Recibido: {data.decode()}")

# Cerrar la conexión
client_socket.close()