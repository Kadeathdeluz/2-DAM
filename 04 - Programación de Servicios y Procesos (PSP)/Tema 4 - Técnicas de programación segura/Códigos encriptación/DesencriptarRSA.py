from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from pathlib import Path

fichero_path = Path(__file__).parent / "DatosEncriptados.bin"

file_open = open(fichero_path,"rb") #abrimos el fichero encriptado

fichero_path = Path(__file__).parent / "privada_usuario_A.pem"

private_key = RSA.import_key(open(fichero_path).read()) #leemos la clave privada del usuario_A

enc_session_key = file_open.read(private_key.size_in_bytes())
nonce = file_open.read(16) #leemos el número generado aleatoriamente para un sólo uso para esta operación de cifrado
tag = file_open.read(16) #leemos el Hash del texto cifrado
cipherTexto = file_open.read() #Ya lo que queda en el fichero es el texto cifrado

# Desencriptar la sesión RSA con la clave privada del usuario
cipher_rsa = PKCS1_OAEP.new(private_key) #Creamos un nuevo objeto con el algoritmo PKCS1_OAEP y la clave RSA
session_key = cipher_rsa.decrypt(enc_session_key)

#Desenecriptamos los datos que se habían encriptado con el algoritmo AES
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(cipherTexto,tag) #Compara el Hash que opbtiene con el Hash que le pasamos para verifiar que los datos no se han modificado
print(data.decode("utf-8"))
