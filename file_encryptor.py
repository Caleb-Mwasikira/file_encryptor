import os
import re
import argparse
import getpass
from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

from file_navigator import FileNavigator


class Encryptor:
    def __init__(self, process, password):
        self.process = process
        self.password = password.encode("utf-8")

        self.key, self.salt = self.keyDerivationFunc(
            salt=b'\x1c\x16\x83|O\xe7^\x7f\xd3\x94G\x00"\xfb\xbdF', # substitute harcoded salt during production
            password=self.password
        )
        self.fernet_cipher = Fernet(self.key)


    def keyDerivationFunc(self, password, salt=None):
        if salt is None:
            BYTES = 16
            salt = os.urandom(BYTES)
            

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = b64encode(kdf.derive(self.password))
        return [key, salt]

    def encryptFile(self, file):
        """Encrypts files using a generated cipher"""

        print(f"[*] Encrypting Data From [ {file} ]")
        with open(file, 'rb') as f:
            data = f.read()

        plain_text = self.fernet_cipher.encrypt(data)

        # Marking the file as (encrypted)
        new_filename = self.renameFile(file)
        
        with open(new_filename, 'wb') as f:
            f.write(plain_text)

        print(f"[+] File Encrypted Successfully\n")


    def decryptFile(self, file):
        """Decrypts files using a generated cipher"""

        print(f"[*] Decrypting Data From [ {file} ]")
        with open(file, 'rb') as f:
            data = f.read()

        try:
            plain_text = self.fernet_cipher.decrypt(data)

            # Marking the file as decrypted
            new_filename = self.renameFile(file)
            with open(new_filename, 'wb') as f:
                f.write(plain_text)

            print(f"[+] File Decrypted Successfully\n")

        except InvalidToken:
            print(f"[!] Error: Using invalid key to decrypt file.\n"
                    "    Please check your password and try again")

    def renameFile(self, file):
        old_file_dirname = os.path.dirname(file)
        old_file_basename = os.path.basename(file)

        if self.process in encrypt:
            new_file_basename = '(encrypted)' + os.path.basename(file)
        else:
            new_file_basename = old_file_basename[11:]
        
        new_filename = os.path.join(old_file_dirname, new_file_basename)
        os.remove(file)
        return new_filename
    


def getProgramArgs():
    """Gets program arguments set when starting the program"""

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--process', help=f"Process to be executed by [ {__file__} ]:\n"
                                                         f"{encrypt} or {decrypt}")
    arg_parser.add_argument('-f', '--filepath', help="Path of the file/folder to be encrypted")
    args = vars(arg_parser.parse_args())
    return [args['process'], args['filepath']]


def fileIsEncrypted(file):
        """Checks whether file is marked as encrypted or not"""

        pattern = re.compile(r'[(]encrypted[)]\w+\.\w+')
        file_is_encrypted = re.match(pattern, os.path.basename(file)) or False
        return file_is_encrypted

def validateUserInput(process, filepath, password):
    confirm_password = ""
    file_exists = False

    while process not in accepted_user_entries:
        print(f"\n[-] No process defined to be executed by [ {__file__} ]:\n"
              f"    Available options: {encrypt} or {decrypt}")
        process= input(">> ")

    while filepath is None or not file_exists:
        filepath = input(f"Please enter the path of the file/files you wish to process >> ")
        file_exists = os.path.exists(filepath)

        if not file_exists:
            print(f"[-] FileNotFound: [ {filepath} ]\n")

    while password is None or len(password) < 1 or password != confirm_password:
        password = getpass.getpass(prompt="Please enter your password >> ")
        confirm_password = getpass.getpass(prompt="Confirm password >> ")

        if password != confirm_password:
            print(f"[-] Error: Password and password confirm DO NOT MATCH")    

    return [process, filepath, password]


def Main():
    global encrypt, decrypt, accepted_user_entries

    process, filepath = getProgramArgs()
    password = os.environ.get("PASSWORD")

    process, filepath, password = validateUserInput(
        process=process, filepath=filepath, password=password
    )

    file_encryptor = Encryptor(process=process, password=password)
    file_navigator = FileNavigator(filepath)
    files = file_navigator.dirList()

    if len(files) == 0:
        print(f"[?] No files found in [ {filepath} ] to encrypt/decrypt.\n"
                "    Please check if filepath is correct and try again\n"
        )

    for file in files:
        if process in encrypt:
            if fileIsEncrypted(file):
                print(f"[!] Cannot encrypt [ {file} ]. File already marked as encrypted\n")
            else:
                file_encryptor.encryptFile(file)
        else:
            if fileIsEncrypted(file):
                file_encryptor.decryptFile(file)
            else:
                print(f"[!] Cannot decrypt [ {file} ]. File already marked as decrypted.\n")
        

if __name__ == "__main__":
    encrypt = ['encrypt', 'e', 'E']
    decrypt = ['decrypt', 'd', 'D']
    accepted_user_entries = encrypt + decrypt

    Main()