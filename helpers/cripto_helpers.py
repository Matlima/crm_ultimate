import os
from cryptography.fernet import Fernet, InvalidToken
from config import CRIPTO_KEY

'''
# Gerar uma chave
key = Fernet.generate_key()
print(key)  # Armazene a chave com segurança, não inclua no código fonte

# Salvar a chave em um arquivo seguro
with open('chave.key', 'wb') as chave_file:
    chave_file.write(key)
'''

# Função para obter a chave de criptografia da variável de ambiente
def get_secret_key():
    key = CRIPTO_KEY
    if key is None:
        raise ValueError("A chave secreta não está definida na variável de ambiente.")
    return key.encode()


# Função para criptografar dados
def encrypt_data(data: str) -> bytes:
    key = get_secret_key()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data


# Função para descriptografar dados
def decrypt_data(encrypted_data: bytes) -> str:
    key = get_secret_key()
    cipher = Fernet(key)
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode()
    except InvalidToken:
        return None

