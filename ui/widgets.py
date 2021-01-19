import os
import getpass
import enum
from PyQt5.QtWidgets import \
    (QWidget, QPushButton, QFileDialog, QLabel, QMenuBar, QAction,
     QLineEdit, QComboBox, QListWidget, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt


class QtLineEdit(enum.Enum):
    """
    0 = Displays chars as they are entered
    1 = Do not display anything
    2 = Display asterisks instead of chars actually entered
    3 = Display chars as they are entered otherwise display asterisks
    """
    Normal = 0
    NoEcho = 1
    Password = 2
    PasswordEchoOnEdit = 3


class ContextMenuPolicy(enum.Enum):
    """
    0, 4 = the widget does not feature a context menu
    1 = the widget's QWidget::contextMenuEvent() handler is called.
    2 = the widget displays its QWidget::actions() as context menu.
    3 = the widget emits the QWidget::customContextMenuRequested() signal.
    """
    NoContextMenu = 0
    DefaultContextMenu = 1
    ActionsContextMenu = 2
    CustomContextMenu = 3
    PreventContextMenu = 4


class Widgets(QWidget):

    def __init__(self):
        super().__init__()
        self.files = []
        self.list_widget = self.line_edit = self.progress_bar = None


    def contextMenu(self, reloadWindowFunction, quitWindowFunction):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        refresh_action = QAction("Refresh", self)
        self.addAction(refresh_action)
        refresh_action.triggered.connect(reloadWindowFunction)

        quit_action = QAction("Quit", self)
        self.addAction(quit_action)
        quit_action.triggered.connect(quitWindowFunction)

    def textLabel(self, dialog: str, position: tuple):
        text_label = QLabel(self)
        text_label.setText(dialog)
        text_label.move(position[0], position[1])

    def listWidget(self, position: tuple):
        self.list_widget = QListWidget(self)
        self.list_widget.move(position[0], position[1])
        self.list_widget.resize(330, 200)
        self.list_widget.dragDropMode()

    def lineEdit(self, position: tuple):
        self.line_edit = QLineEdit(self)
        self.line_edit.setEchoMode(QtLineEdit.Password.value)
        self.line_edit.move(position[0], position[1])
        self.line_edit.textChanged.connect(self.onChangedLineEdit)

    def qPushButton(self, btn_name: str, position: tuple, connect_function):
        btn = QPushButton(btn_name, self)
        btn.move(position[0], position[1])
        btn.clicked.connect(connect_function)

    def comboBox(self, items: list, position: tuple):
        combo = QComboBox(self)
        for item in items:
            combo.addItem(item)

        combo.move(position[0], position[1])
        combo.activated[str].connect(self.onChangedComboBox)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select file you wish to encrypt/decrypt", "",
                                                   "All Files (*)", options=options)
        if file_name:
            index = 0
            self.list_widget.insertItem(index, file_name)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = os.path.abspath(f"/home/{getpass.getuser()}/")
        files, _ = QFileDialog.getOpenFileNames(self, "Select files you wish to encrypt/decrypt", directory,
                                                "All Files (*)", options=options)
        if files:
            self.files = files
            for file in files:
                index = files.index(file)
                self.list_widget.insertItem(index, file)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "",
                                                   "All Files (*)", options=options)
        if file_name:
            self.files = file_name

    def messageBoxDialog(self, dialog: str):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(dialog)
        msg_box.setWindowTitle("Input Error")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.exec()

    def progressBar(self, position: tuple, size: tuple, value: int = 0):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(position[0], position[1], size[0], size[1])
        self.progress_bar.setValue(value)
        self.progress_bar.hide()
