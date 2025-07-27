from cryptography.fernet import Fernet
import os

# Load encryption key from environment variable or file
ENCRYPTION_KEY_PATH = os.getenv("ENCRYPTION_KEY_PATH", "encryption_key.key")

def load_encryption_key():
    if os.getenv("ENCRYPTION_KEY"):  # Load from environment variable if available
        return os.getenv("ENCRYPTION_KEY").encode()

    if os.path.exists(ENCRYPTION_KEY_PATH):
        with open(ENCRYPTION_KEY_PATH, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_PATH, "wb") as key_file:
            key_file.write(key)
        return key

encryption_key = load_encryption_key()
cipher = Fernet(encryption_key)

def encrypt_data(data):
    """Encrypts a string using Fernet encryption."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypts a string using Fernet encryption."""
    try:
        return cipher.decrypt(encrypted_data.encode()).decode()
    except Exception:
        return "Decryption error: Invalid or corrupted data"
