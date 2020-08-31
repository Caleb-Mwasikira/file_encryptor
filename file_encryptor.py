from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os
import re
import base64
import argparse
import getpass

from file_navigator import FileNavigator

class Encryptor:
    """Encrypts And Decrypts Files Based On the Users Input Password"""
    def __init__(self, filepath, password):
        """Generates Symmetric Key That Will Be Used In Encryption And Decryption"""
        self.password = password

        # Use self.salt = os.urandom(10) for production.
        self.salt = b'\x1c\x16\x83|O\xe7^\x7f\xd3\x94G\x00"\xfb\xbdF'
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )

        self.key = base64.b64encode(self.kdf.derive(self.password.encode("utf-8")))
        self.file = filepath

    def encryptFile(self):
        """Encrypts files using a password"""

        print(f"[*] Encrypting Data From {self.file}")
        with open(self.file, 'rb') as f:
            data = f.read()

        f = Fernet(self.key)
        encrypted_data = f.encrypt(data)

        # Adding a naming convention (encrypted) to mark file as already encrypted
        old_file_dirname = os.path.dirname(self.file)
        new_file_basename = '(encrypted)' + os.path.basename(self.file)
        new_filename = os.path.join(old_file_dirname, new_file_basename)

        with open(new_filename, 'wb') as f:
            f.write(encrypted_data)

        os.remove(self.file)
        print(f'[+] File Encrypted Successfully')

    def decryptFile(self):
        """Decrypts (encrypted) files using a password"""
        print(f"[*] Decrypting Data From {self.file}")
        with open(self.file, 'rb') as f:
            data = f.read()

        f = Fernet(self.key)
        plaintext = f.decrypt(data)

        # Removing the naming convention (encrypted) that was placed when file was being encrypted
        old_file_dirname = os.path.dirname(self.file)
        old_file_basename = os.path.basename(self.file)

        new_file_basename = old_file_basename[11:]

        new_file_name = os.path.join(old_file_dirname, new_file_basename)
        with open(new_file_name, 'wb') as f2:
            f2.write(plaintext)

        os.remove(self.file)
        print(f'[+] File Decrypted Successfully')

def getProgramArgs():
    """Gets system arguments set when starting the program"""
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-p', '--process', help=f"Process to be executed by {__file__}:\n"
                                                         f"{encrypt} or {decrypt}")
    argument_parser.add_argument('-f', '--filepath', help="Path of the file/folder to be encrypted")
    args = vars(argument_parser.parse_args())
    return [args['process'], args['filepath']]

def Main(process, file, password):
    encryptor = Encryptor(filepath=file, password=password)

    pattern = re.compile(r'[(]encrypted[)]\w+\.\w+')
    file_is_encrypted = re.match(pattern, os.path.basename(file)) or False

    if process in encrypt:
        if file_is_encrypted:
            print("[!] Error: Trying to encrypt an encrypted file!")
        else:
            encryptor.encryptFile()
    else:
        if file_is_encrypted:
            encryptor.decryptFile()
        else:
            print("[!] Error: Trying to decrypt a decrypted file!")

if __name__ == "__main__":
    encrypt = ['encrypt', 'e', 'E']
    decrypt = ['decrypt', 'd', 'D']
    accepted_user_entries = encrypt + decrypt

    process, filepath = getProgramArgs()
    password = os.environ.get("PASSWORD")

    if process not in accepted_user_entries:
        print(f"[-] Error: Invalid process to be executed by {__file__}:\n"
              f"    Available options: -p {encrypt} or -p {decrypt}")
        exit()

    while password is None or len(password) < 1:
        password = getpass.getpass(prompt="Please Enter your password: ")

    fileNavigator = FileNavigator(filepath)
    dir_list = fileNavigator.dirList()

    if len(dir_list) < 1:
        print(f"[!] Error: {filepath} does not exist")
    else:
        for file in dir_list:
            Main(process=process, file=file, password=password)

