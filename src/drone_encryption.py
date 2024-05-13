import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import logging

class DroneEncryption:
    """
    Handles RSA and Fernet encryption for secure data transmission between the drone and its control systems,
    with enhanced user controls and robust error handling.
    """
    def __init__(self, private_key_path=None, public_key_path=None):
        self.logger = self.setup_logging()
        try:
            if private_key_path and public_key_path:
                self.private_key = self.load_private_key(private_key_path)
                self.public_key = self.load_public_key(public_key_path)
            else:
                self.private_key, self.public_key = self.generate_keys()
                self.logger.info("New RSA keys generated.")
            self.fernet_key = Fernet.generate_key()
            self.fernet = Fernet(self.fernet_key)
            self.logger.info("Fernet key generated.")
        except Exception as e:
            self.logger.error(f"Encryption setup failed: {str(e)}")
            raise

    def setup_logging(self):
        """
        Set up a logger for encryption processes.
        """
        logger = logging.getLogger('DroneEncryptionHandler')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('drone_encryption.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def generate_keys(self):
        """
        Generate RSA public and private keys with error handling.
        """
        try:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
            public_key = private_key.public_key()
            return private_key, public_key
        except Exception as e:
            self.logger.error(f"Failed to generate keys: {str(e)}")
            raise

    def load_private_key(self, file_path):
        """
        Load an RSA private key from a file with error handling.
        """
        if not os.path.exists(file_path):
            self.logger.error(f"Private key file not found at {file_path}")
            raise FileNotFoundError(f"No private key found at the specified path: {file_path}")
        with open(file_path, 'rb') as key_file:
            try:
                private_key = load_pem_private_key(key_file.read(), password=None, backend=default_backend())
                return private_key
            except Exception as e:
                self.logger.error(f"Failed to load private key: {str(e)}")
                raise

    def load_public_key(self, file_path):
        """
        Load an RSA public key from a file with error handling.
        """
        if not os.path.exists(file_path):
            self.logger.error(f"Public key file not found at {file_path}")
            raise FileNotFoundError(f"No public key found at the specified path: {file_path}")
        with open(file_path, 'rb') as key_file:
            try:
                public_key = load_pem_public_key(key_file.read(), backend=default_backend())
                return public_key
            except Exception as e:
                self.logger.error(f"Failed to load public key: {str(e)}")
                raise

    def rsa_encrypt(self, message):
        """
        Encrypt a message using RSA public key encryption with error handling.
        """
        try:
            encrypted_message = self.public_key.encrypt(
                message.encode(),
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            return encrypted_message
        except Exception as e:
            self.logger.error(f"RSA encryption failed: {str(e)}")
            raise

    def rsa_decrypt(self, encrypted_message):
        """
        Decrypt a message using RSA private key encryption with error handling.
        """
        try:
            decrypted_message = self.private_key.decrypt(
                encrypted_message,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            return decrypted_message.decode()
        except Exception as e:
            self.logger.error(f"RSA decryption failed: {str(e)}")
            raise

    def fernet_encrypt(self, message):
        """
        Encrypt a message quickly using Fernet symmetric encryption with error handling.
        """
        try:
            return self.fernet.encrypt(message.encode())
        except Exception as e:
            self.logger.error(f"Fernet encryption failed: {str(e)}")
            raise

    def fernet_decrypt(self, encrypted_message):
        """
        Decrypt a message quickly using Fernet symmetric encryption with error handling.
        """
        try:
            return self.fernet.decrypt(encrypted_message).decode()
        except Exception as e:
            self.logger.error(f"Fernet decryption failed: {str(e)}")
            raise

# Example usage can be:
# encryption = DroneEncryption()
# encrypted_msg = encryption.rsa_encrypt('Hello, Drone!')
# print("Encrypted:", encrypted_msg)
# decrypted_msg = encryption.rsa_decrypt(encrypted_msg)
# print("Decrypted:", decrypted_msg)

