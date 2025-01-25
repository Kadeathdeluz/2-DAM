import requests
import json

# URL base de la API JSONPlaceholder para recursos de prueba (hay otas bases de datos de prueba: posts, comments, photos, albums)
base_url = "https://jsonplaceholder.typicode.com/todos"

# Método GET para obtener información sobre tareas
def get_tarea():
    respuesa = requests.get(base_url)
    if respuesa.status_code == 200:
        tarea = respuesa.json()
        print("Lista de tareas:")
        for i in tarea:
            print(f"ID: {i['id']}, Nombre: {i['title']}, Finalizada: {i['completed']}")
    else:
        print(f"Error al obtener tareas. Código de estado: {respuesa.status_code}")

# Método POST para crear una nueva tarea
def create_tarea(nombre, finalizada):
    nueva_tarea = {"title": nombre, "completed": finalizada}
    headers = {"Content-Type": "application/json"}
    respuesta = requests.post(base_url, data=json.dumps(nueva_tarea), headers=headers)
    if respuesta.status_code == 201:
        print("Tarea creada exitosamente.")
    else:
        print(f"Error al crear la tarea. Código de estado: {respuesta.status_code}")

# Método PUT para actualizar una tarea existente (asumiendo que existe una tarea con ID 1)
def update_tarea(id_tarea, nuevo_nombre):
    update_data = {"title": nuevo_nombre}
    headers = {"Content-Type": "application/json"}
    update_url = f"{base_url}/{id_tarea}"
    respuesta = requests.put(update_url, data=json.dumps(update_data), headers=headers)
    if respuesta.status_code == 200:
        print(f"Tarea actualizada exitosamente.")
    else:
        print(f"Error al actualizar la tarea. Código de estado: {respuesta.status_code}")

def delete_tarea(id_tarea):
    delete_url = f"{base_url}/{id_tarea}"
    respuesta = requests.delete(delete_url)
    if respuesta.status_code == 200:
        print(f"Tarea eliminada exitosamente.")
    else:
        print(f"Error al eliminar la tarea. Código de estado: {respuesta.status_code}")

# Ejemplo de uso
get_tarea()
create_tarea("Nueva Tarea", False)
update_tarea(1, "Prueba de API")
delete_tarea(1)
