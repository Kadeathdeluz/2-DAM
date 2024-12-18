import socket

def pedir_página_web(socket,web_path):
    """Obtiene y muestra por pantalla una página web del path solicitado."""

    # Formateamos el mensaje de solicitud HTTP GET
    peticion = f'GET {web_path} HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n'

    try:
        # Enviamos la petición al servidor
        socket.sendall(peticion.encode())
        # Recibimos y mostramos la respuesta del servidor
        mensaje = socket.recv(2048) #El tamaño del mensaje es 1616 Bytes, por lo que con un buffer de 2048, podrá descargar la página completa
        # Mostramos la respuesta del servidor
        print(mensaje.decode())
    except socket.error as exc:
        print ("Excepción de socket: %s" % exc)
        raise
    finally:
        socket.close()


if __name__ ==  "__main__":
    # Configuración del servidor web
    web_host = "example.com"
    web_port = 80
    web_path = "/" #solicitamos la página principal, la raiz

    try:
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as exc:
        print ("Error al crear el socket: %s" % exc)
        raise
    
    try:
        socket_cliente.connect((web_host,web_port))
    except socket.error as exc:
        print ("Error al conectr el socket: %s" % exc)
        raise
    print('Conectado con éxito')

    pedir_página_web(socket_cliente,web_path)

    