import re
from base64 import b64encode
from os import urandom, path, remove

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken


encrypt = ['encrypt', 'e', 'E', 'Encrypt']
decrypt = ['decrypt', 'd', 'D', 'Decrypt']


class Encryptor:
    def __init__(self, action, password):

        self.action = action
        password = password.encode("utf-8")

        self.key, self.salt = self.keyDerivationFunc(
            salt=b'\x1c\x16\x83|O\xe7^\x7f\xd3\x94G\x00"\xfb\xbdF',  # substitute hardcoded salt during production
            password=password
        )
        self.fernet_cipher = Fernet(self.key)

    @staticmethod
    def keyDerivationFunc(password, salt=None):
        if salt is None:
            BYTES = 16
            salt = urandom(BYTES)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = b64encode(kdf.derive(password))
        return [key, salt]

    def encryptFile(self, file):
        """Encrypts files using a generated cipher"""

        print(f"[*] Encrypting Data From [ {file} ]")
        with open(file, 'rb') as f:
            data = f.read()

        cipher_text = self.fernet_cipher.encrypt(data)

        # Marking the file as (encrypted)
        new_filename = self._renameFile(file)

        with open(new_filename, 'wb') as f:
            f.write(cipher_text)

        print(f"[+] File Encrypted Successfully\n")
        return True

    def decryptFile(self, file):
        """Decrypts files using a generated cipher"""

        print(f"[*] Decrypting Data From [ {file} ]")
        with open(file, 'rb') as f:
            data = f.read()

        try:
            plain_text = self.fernet_cipher.decrypt(data)

            # Marking the file as decrypted
            new_filename = self._renameFile(file)
            with open(new_filename, 'wb') as f:
                f.write(plain_text)

            print(f"[+] File Decrypted Successfully\n")
            return True

        except InvalidToken:
            print(f"[!] Error: Using invalid key to decrypt file.\n"
                  "    Please check your password and try again")
            return False

    def _renameFile(self, file):  # this is a private method
        old_file_dirname = path.dirname(file)
        old_file_basename = path.basename(file)

        if self.action in encrypt:
            new_file_basename = '(encrypted)' + path.basename(file)
        else:
            new_file_basename = old_file_basename[11:]

        new_filename = path.join(old_file_dirname, new_file_basename)
        remove(file)
        return new_filename

    @staticmethod
    def fileIsEncrypted(file):
        """Checks whether file is marked as encrypted or not"""

        pattern = re.compile(r"[(]encrypted[)]")
        file_is_encrypted = re.match(pattern, path.basename(file)) or False
        return file_is_encrypted
