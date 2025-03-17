from Crypto.PublicKey import RSA
from pathlib import Path

key = RSA.generate(2048) #creamos la llave privada RSA

private_key = key.exportKey() #codifica la clave en un formato que se pueda exportar a un fichero

fichero_path = Path(__file__).parent / "privada_servidor.pem" #forzamos que el fichero se guarde junto a nuestro ejecutable py

file_out = open(fichero_path,"wb")
file_out.write(private_key) #escribimos la clave formateada en un fichero pem
file_out.close()

public_key = key.publickey().exportKey() #generamos la clave pública a partir de la clave privada

fichero_path = Path(__file__).parent / "publica_servidor.pem" #forzamos que el fichero se guarde junto a nuestro ejecutable py

file_out = open(fichero_path,"wb")
file_out.write(public_key) #escribimos la clave pública en otro fichero
file_out.close()
