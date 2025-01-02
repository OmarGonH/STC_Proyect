# -*- coding: utf-8 -*-
"""Shamir y AES.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EpCy7JrCq2j2fYkCp7GGf1oiJouNlaS3
"""

!pip install pyshamir

from pyshamir import split, combine
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Función para cifrar el texto con AES 128-GCM
def encrypt_aes_gcm(key, data):
    # Generar un nonce aleatorio de 12 bytes
    nonce = os.urandom(12)

    # Crear un cifrador AES en modo GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    # Cifrar los datos (sin padding, ya que GCM lo maneja automáticamente)
    ciphertext = encryptor.update(data) + encryptor.finalize()

    # Devuelve el nonce, el texto cifrado y el tag (autenticación)
    return nonce, ciphertext, encryptor.tag

# Función para descifrar con AES 128-GCM
def decrypt_aes_gcm(key, nonce, ciphertext, tag):
    # Crear un descifrador AES en modo GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Descifrar los datos (sin necesidad de unpadder porque GCM no requiere padding)
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_data

# generate a random secret, here secret is a 128 bytes key for AES
secret = secrets.token_bytes(16)  # 128 bits (16 bytes)

# Solicitar al usuario el número de partes para dividir el secreto
num_of_shares = int(input("Introduce el número de partes para dividir el secreto: "))

# Calcular el umbral como la mitad del número de partes + 1
threshold = num_of_shares // 2 + 1

# split to get a list of bytearrays which can be combined later to get back the secret
parts = split(secret, num_of_shares, threshold)

print("Secreto original:", secret.hex())
print("Umbral:", threshold)

# Solicitar al usuario un umbral para realizar el descifrado
user_threshold = int(input(f"Introduce un umbral (debe ser igual o mayor que {threshold}): "))

# Verificar si el umbral ingresado es igual o mayor al umbral definido en el código
if user_threshold >= threshold:
    # Ahora, las partes pueden combinarse para recuperar el secreto
    recomb_secret = combine(parts)

    # Imprimir el contenido del bytearray como hexadecimal
    print("Secreto recombinado (contenido del bytearray):", recomb_secret.hex())

    # Verificar si el secreto original y el recombinado son iguales
    if secret == recomb_secret:
        print("La llave reconstruida es exactamente la misma que la original.")

        # Cifrar un documento o un mensaje con la llave generada
        data = b"Este es un documento secreto."  # Ejemplo de contenido
        nonce, ciphertext, tag = encrypt_aes_gcm(secret, data)
        print("Texto cifrado:", ciphertext.hex())

        # Usar la llave reconstruida para descifrar
        decrypted_data = decrypt_aes_gcm(recomb_secret, nonce, ciphertext, tag)
        print("Texto descifrado:", decrypted_data.decode())

    else:
        print("La llave reconstruida NO es igual a la original.")
else:
    print(f"No se puede realizar el descifrado. El umbral ingresado ({user_threshold}) es menor que el umbral requerido ({threshold}).")

from pyshamir import split, combine
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Función para cifrar el texto con AES 128-GCM
def encrypt_aes_gcm(key, data):
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return nonce, ciphertext, encryptor.tag

# Función para descifrar con AES 128-GCM
def decrypt_aes_gcm(key, nonce, ciphertext, tag):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data

# Generar una clave AES de 128 bits
secret = secrets.token_bytes(16)

# Solicitar al usuario el número de partes para dividir el secreto
num_of_shares = int(input("Introduce el número de partes para dividir el secreto: "))

# Calcular el umbral como la mitad del número de partes + 1
threshold = num_of_shares // 2 + 1

# Dividir el secreto en partes
parts = split(secret, num_of_shares, threshold)

print("Secreto original:", secret.hex())
print("Umbral:", threshold)

# Guardar cada pedazo de la clave en un archivo
for i, part in enumerate(parts):
    filename = f"part_{i+1}.bin"
    with open(filename, "wb") as file:
        file.write(part)
    print(f"Parte {i+1} guardada en {filename}")

# Solicitar al usuario un umbral para realizar el descifrado
user_threshold = int(input(f"Introduce un umbral (debe ser igual o mayor que {threshold}): "))

# Verificar si el umbral ingresado es igual o mayor al umbral definido en el código
if user_threshold >= threshold:
    recomb_secret = combine(parts)
    print("Secreto recombinado (contenido del bytearray):", recomb_secret.hex())

    if secret == recomb_secret:
        print("La llave reconstruida es exactamente la misma que la original.")

        # Cifrar un documento o un mensaje con la llave generada
        data = b"/content/2021630283 Constancia de Estudios 2024-09-24.pdf"
        nonce, ciphertext, tag = encrypt_aes_gcm(secret, data)
        print("Texto cifrado:", ciphertext.hex())

        # Usar la llave reconstruida para descifrar
        decrypted_data = decrypt_aes_gcm(recomb_secret, nonce, ciphertext, tag)
        print("Texto descifrado:", decrypted_data.decode())

    else:
        print("La llave reconstruida NO es igual a la original.")
else:
    print(f"No se puede realizar el descifrado. El umbral ingresado ({user_threshold}) es menor que el umbral requerido ({threshold}).")