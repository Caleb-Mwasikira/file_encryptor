import sys
from PyQt5.QtWidgets import QApplication

from ui.widgets import Widgets
from custom_packages.encryptor import Encryptor, encrypt, decrypt


class MainWindow(Widgets):

    def __init__(self):
        super().__init__()
        self.action = self.password = None

        self.initUI()

    def initUI(self):
        self.textLabel("Welcome to file_encryptor.", (30, 30))

        self.contextMenu(self.reloadWindow, self.quitWindow)

        self.comboBox(["Encrypt", "Decrypt"], (30, 70))
        self.qPushButton("Select File", (30, 120), self.openFileNamesDialog)
        self.listWidget((150, 70))

        self.textLabel("Enter your password: ", (30, 300))
        self.lineEdit((200, 300))
        self.qPushButton('Ok', (30, 350), self.processUserData)
        self.progressBar((30, 400), (200, 25), 0)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("File Encryptor")
        self.show()

    def onChangedLineEdit(self, text):
        self.password = text

    def onChangedComboBox(self, text):
        self.action = text

    def reloadWindow(self):
        self.list_widget.clear()
        self.line_edit.clear()

        self.files = []
        self.progress_bar.hide()
        self.action = self.password = None

    @staticmethod
    def quitWindow():
        QApplication.quit()

    def processUserData(self):
        if self.action is None:
            self.messageBoxDialog("Please enter action you wish to take. Encrypt | Decrypt")

        elif not self.files:
            self.messageBoxDialog("No files selected for encryption/decryption")

        elif self.password is None:
            self.messageBoxDialog("Please enter the password for encryption/decryption")

        elif len(self.password) < 8:
            self.messageBoxDialog(f"Minimum password length is 8 characters. {len(self.password)} chars given")

        else:
            self.progress_bar.show()
            self.list_widget.clear()
            self.processFiles(self.action, self.password, self.files)

    def processFiles(self, action, password, files):
        encryptor = Encryptor(action, password)

        for file in files:
            index = files.index(file) + 1
            len_files = len(files)
            progress = int((index / len_files) * 100)

            if action in encrypt:
                if encryptor.fileIsEncrypted(file):
                    self.list_widget.insertItem(
                        index, f"[!] Cannot encrypt ( {file} ).\n File already marked as encrypted")
                else:
                    encryptor.encryptFile(file)
                    self.progress_bar.setValue(progress)
                    self.list_widget.insertItem(index, f"File ( {file} ) encrypted successfully")

            if action in decrypt:
                if encryptor.fileIsEncrypted(file):
                    encryptor.decryptFile(file)
                    self.progress_bar.setValue(progress)
                    self.list_widget.insertItem(index, f"File ( {file} ) decrypted successfully")
                else:
                    self.list_widget.insertItem(
                        index, f"[!] Cannot decrypt ( {file} ). File already marked as decrypted.\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
