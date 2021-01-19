import argparse

from custom_packages.encryptor import Encryptor, encrypt, decrypt
from custom_packages import cli


def getProgramArgs():
    """Gets program arguments set when starting the program"""

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-a', '--action', help=f"action to be executed by [ {__file__} ]:\n"
                                                   f"{encrypt} or {decrypt}")
    arg_parser.add_argument('-f', '--filepath', help="Path of the file/folder to be encrypted")
    args = vars(arg_parser.parse_args())

    action = args['action'] or cli.getUserAction()
    file_path = args['filepath'] or cli.getFilePath()
    username, password = cli.getUserAuthInfo()
    return [username, password, action, file_path]


def Main():
    username, password, action, file_path = getProgramArgs()
    selected_files = cli.getSelectedFiles(file_path)
    encryptor = Encryptor(action, password)

    if action in encrypt:
        for file in selected_files:
            if encryptor.fileIsEncrypted(file):
                print(f"[!] Cannot encrypt [ {file} ]. File already marked as encrypted\n")
            else:
                encryptor.encryptFile(file)
    else:
        for file in selected_files:
            if encryptor.fileIsEncrypted(file):
                encryptor.decryptFile(file)
            else:
                print(f"[!] Cannot decrypt [ {file} ]. File already marked as decrypted.\n")


if __name__ == "__main__":
    Main()
