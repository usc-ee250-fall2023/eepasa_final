from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode
import os

"""
def make_key():
    # Generate a random 256-bit AES key
    key = os.urandom(32)



    return key
def make_iv():
    # Generate a random 128-bit IV
    iv = os.urandom(16)

    return iv
"""

key = b'12345678909876543212345678909876'
iv = b'1234567890987654'

def Encrypt(message, key, iv):
    message = str(message)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return b64encode(ciphertext).decode()

def Decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(b64decode(ciphertext)) + decryptor.finalize()
    return decrypted_message.decode()

#key = make_key()
#sssiv = make_iv()
#og_msg = input()

#encrypt 
#encrypt_msg = Encrypt(og_msg, key, iv)
#print(f"Encrypted message: {encrypt_msg}")

#decrypt 
#decrypt_msg = Decrypt(encrypt_msg, key, iv)
#print(f"Decrypted message: {decrypt_msg}")
