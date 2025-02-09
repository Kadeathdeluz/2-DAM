import socket
import json
import requests
from config import OPENAI_API_KEY, WEATHER_API_KEY  # Importamos las API Keys

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección local
PORT = 65432        # Puerto para la comunicación

# Función para obtener respuesta de OpenAI (ChatGPT), Openai es de pago y no muestra respuestas, únicamente da error
def get_gpt_response(question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [{"role": "user", "content": question}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error en la respuesta de la IA.")

# Función para obtener respuesta de DeepSeek: he intentado obtener API Key pero no he podido
def get_deepseek_response(question):
    return "DeepSeek aún no está disponible"

# Función para obtener el clima desde OpenWeather
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") != 200:
        return f"Error: {data.get('message', 'No se encontró información')}"
    
    weather_info = {
        "ciudad": data["name"],
        "temperatura": f"{data['main']['temp']}°C",
        "clima": data["weather"][0]["description"],
        "humedad": f"{data['main']['humidity']}%"
    }
    return weather_info

# Inicia el servidor y espera conexiones
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Conectado con {addr}")
                data = conn.recv(1024)
                if not data:
                    break

                request = json.loads(data.decode())
                response = {}

                match request["tipo"]:
                    case "gpt":
                        response["respuesta"] = get_gpt_response(request["pregunta"])
                    
                    case "deepseek":
                        response["respuesta"] = "DeepSeek aún no está disponible"
                    
                    case "clima":
                        response["respuesta"] = get_weather(request["ciudad"])
                    
                    case _:
                        response["error"] = "Tipo de consulta no válido"

                conn.sendall(json.dumps(response).encode())
