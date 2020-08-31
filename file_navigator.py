import os

class FileNavigator:
    """Returns all files in a directory if dir exists or False if dir does NOT exist"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_exists = os.path.exists(filepath)

    def dirList(self):
        if os.path.isfile(self.filepath):
            return [os.path.abspath(self.filepath)]
        else:
            dir_list = []
            for root, dirs, files in os.walk(self.filepath, topdown=True):
                for file in files:
                    dir_list.append(os.path.abspath(os.path.join(root, file)))
            return dir_list

if __name__=="__main__":
    File_navigator= FileNavigator('./data')
    print(File_navigator.dirList())

