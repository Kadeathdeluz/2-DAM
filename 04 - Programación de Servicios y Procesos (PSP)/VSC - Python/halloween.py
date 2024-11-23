
diccionario_pociones = {
        "p_invisibilidad": ['ojo de tritón', 'cola de rata', 'escamas de serpiente'],
        "p_fuego_infernal":['polvo de murciélago', 'cenizas de dragón', 'sangre de vampiro'],
        "p_curativa":['hierba lunar', 'escamas de serpiente', 'lágrimas de fénix'],
        "p_teletrans":['polvo de hadas',  'pluma de buho', 'cenizas de dragon']
}

lista_alergenos = ['escama', 'rata', 'buho']



if __name__ == "__main__":

    entrada = input("Proporciona una lista de ingredientes (separados por comas)").lower().split(',')

    lista_ingredientes = [ingrediente.strip() for ingrediente in entrada]

    for ingrediente in lista_ingredientes:
        for pocion in diccionario_pociones:
            if ingrediente in pocion:
                print(f"{pocion} contiene {ingrediente}")
# Para comprobar que están todos los ingredientes de la poción
all()