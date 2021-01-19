import os
import inquirer
from pprint import pprint
from inquirer import errors

from custom_packages import file_navigator

"""
cli.py short for (command line interface).py is responsible for 
asking end user questions, parsing, validating answers, 
managing hierarchical prompts and providing error feedback 
for our file encryption program.
"""


def getUserAuthInfo():
    """This section asks for the users username and password"""
    def validateUserName(_, selected_username):
        if len(selected_username) < 4:
            raise errors.ValidationError('', reason="Username too short")

        return True

    def validatePassword(_, selected_password):
        if len(selected_password) < 6:
            raise errors.ValidationError('', reason="Password too short")
        
        return True

    qsts = [
        inquirer.Text(
            'username', message="Please enter your username",
            validate=validateUserName
        ),
        inquirer.Password(
            "password", message="Please enter your password",
            validate=validatePassword
        )
    ]
    answers: dict = inquirer.prompt(qsts)
    username, password = answers.values()
    return [username, password]


def getUserAction():
    """Asks the user the action they want executed by the program"""
    qst = [
        inquirer.List(
            "action", message="What do you want to do?",
            choices=['Encrypt', 'Decrypt']
        )
    ]
    answer: dict = inquirer.prompt(qst)
    user_action = answer['action']
    return user_action


def getFilePath():
    def validateFilePath(_, current_file_path):
        files_found: list = file_navigator.dirList(current_file_path)

        if not os.path.exists(current_file_path):
            raise errors.ValidationError('', reason=f"Filepath {current_file_path} does not exist")
        elif len(files_found) == 0:
            raise errors.ValidationError('', reason=f"Filepath {current_file_path} has no files to encrypt/decrypt")
        
        return True

    qst = [
        inquirer.Path(
            "filepath", message="Enter the file/folder you want to encrypt/decrypt",
            normalize_to_absolute_path=True, validate=validateFilePath
        )
    ]
    answer: dict = inquirer.prompt(qst)
    file_path = answer['filepath']
    return file_path


def getSelectedFiles(file_path):
    """Gets the files the user would like to encrypt/decrypt"""

    files_found: list = file_navigator.dirList(file_path)
    default_choice = ['SelectAll']

    confirm_qst = [
        inquirer.Checkbox(
            "selected_files", message=f"The following files have been found in {file_path} -> key to select file. <- "
                                      f"key to deselect file.\n",
            choices=default_choice + files_found,
            default=[]
        )
    ]
    confirm_answer = inquirer.prompt(confirm_qst)
    selected_files = confirm_answer['selected_files']

    if selected_files == default_choice:
        selected_files = files_found

    return selected_files


def Main():
    username, password = getUserAuthInfo()
    action = getUserAction()
    file_path = getFilePath()
    selected_files = getSelectedFiles(file_path)
    user_info = dict(
        user= {
            "username": username,
            "password": password
        },
        action= action,
        selected_files= selected_files
    )
    pprint(user_info)


if __name__ == "__main__":
    Main()
    
