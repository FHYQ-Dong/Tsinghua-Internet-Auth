import base64
from Crypto.Cipher import AES

class AESCipher:
    def __init__(self, key):
        self.key = self.__padding(key)

    def __padding(self, raw):
        if len(raw) % 16 != 0:
            return raw + b'\x00' * (16 - len(raw) % 16)
        else:
            return raw

    def __encrypt(self, raw):
        raw = self.__padding(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(raw)

    def __decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(enc).rstrip(b'\x00')
    
    def encrypt_from_str_to_base64(self, data: str) -> str:
        return base64.b64encode(self.__encrypt(data.encode('utf-8'))).decode('utf-8')
    
    def decrypt_from_base64_to_str(self, data: str) -> str:
        return self.__decrypt(base64.b64decode(data)).decode('utf-8')
