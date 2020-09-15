import os


class FileNavigator:
    def __init__(self, filepath):
        self.filepath = filepath

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
    file_navigator= FileNavigator('./data')
    print(file_navigator.dirList())

