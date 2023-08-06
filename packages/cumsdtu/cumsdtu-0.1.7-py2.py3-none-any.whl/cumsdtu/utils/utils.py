import hashlib
class EncryptDecrypt:
    @staticmethod
    def enc_sha1(value:str):
        return hashlib.sha1(value.encode()).hexdigest()

    @staticmethod
    def enc_sha256(value:str):
        return hashlib.sha256(value.encode()).hexdigest()