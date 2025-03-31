from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

class EncryptionModel:
    def encrypt(self, data, key):
        """Encrypt data using AES-128 CBC mode"""
        try:
            key = key.encode('utf-8')[:16].ljust(16, b'\0')
            cipher = AES.new(key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
            iv = cipher.iv
            return base64.b64encode(iv + ct_bytes).decode('utf-8')
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")