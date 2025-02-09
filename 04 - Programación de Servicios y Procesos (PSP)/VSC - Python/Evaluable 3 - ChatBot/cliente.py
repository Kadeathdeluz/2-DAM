import socket
import json

# Configuración del cliente
HOST = '127.0.0.1'  # Dirección del servidor
PORT = 65432        # Puerto del servidor

# Muestra el menú principal y procesa las solicitudes del usuario
def main():
    while True:
        print("\nSeleccione el tipo de consulta:")
        print("1. Pregunta a GPT")
        print("2. Pregunta a DeepSeek")
        print("3. Clima en una ciudad")
        print("4. Salir")
        
        opcion = input("Opción: ")

        match opcion:
            case "1":
                pregunta = input("Pregunta para GPT: ")
                request = {"tipo": "gpt", "pregunta": pregunta}
            
            case "2":
                pregunta = input("Pregunta para DeepSeek: ")
                request = {"tipo": "deepseek", "pregunta": pregunta}

            case "3":
                ciudad = input("Ciudad: ")
                request = {"tipo": "clima", "ciudad": ciudad}

            case "4":
                break

            case _:
                print("Opción no válida.")

        # Enviar la solicitud al servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(request).encode())

            # Recibir la respuesta
            response = client_socket.recv(1024)
            response_data = json.loads(response.decode())

            print("\nRespuesta del servidor:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
