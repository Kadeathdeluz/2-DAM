import socket
"""
3-ways-handshake
CÓDIGO DEL SERVIDOR

"""
# Crear un socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al puerto y la dirección
server_socket.bind(('localhost', 12345))

# Escuchar las solicitudes de conexión
server_socket.listen(1)
print("Esperando conexión...")

# Aceptar una conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conexión establecida con {client_address}")

# Recibir datos del cliente
data = client_socket.recv(1024)
print(f"Recibido: {data.decode()}")

# Enviar una respuesta al cliente
client_socket.sendall("¡Hola, cliente! Conexión establecida.".encode())

# Cerrar la conexión
client_socket.close()
server_socket.close()