import unittest
from unittest.mock import patch, MagicMock
from drone_encryption import DroneEncryption

class TestDroneEncryption(unittest.TestCase):
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('drone_encryption.load_pem_private_key')
    @patch('drone_encryption.load_pem_public_key')
    def setUp(self, mock_load_public_key, mock_load_private_key, mock_exists, mock_open):
        # Configure mocks for keys
        mock_private_key = MagicMock()
        mock_public_key = MagicMock()
        mock_load_private_key.return_value = mock_private_key
        mock_load_public_key.return_value = mock_public_key
        
        # Instance of the DroneEncryption with mocked paths
        self.encryption = DroneEncryption(private_key_path='fake_private.pem', public_key_path='fake_public.pem')

    def test_fernet_encryption_decryption(self):
        # Test Fernet encryption and decryption
        message = "Test message"
        encrypted = self.encryption.fernet_encrypt(message)
        decrypted = self.encryption.fernet_decrypt(encrypted)
        self.assertEqual(decrypted, message)

    def test_rsa_encryption_decryption(self):
        # Mock encryption and decryption process
        self.encryption.public_key.encrypt.return_value = b'encrypted_message'
        self.encryption.private_key.decrypt.return_value = b'Test message'

        encrypted = self.encryption.rsa_encrypt('Test message')
        decrypted = self.encryption.rsa_decrypt(encrypted)
        self.assertEqual(decrypted, 'Test message')

    def test_generate_keys(self):
        # Ensure that keys can be generated
        private_key, public_key = self.encryption.generate_keys()
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)

if __name__ == '__main__':
    unittest.main()
