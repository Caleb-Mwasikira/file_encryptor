from os import path, walk


def dirList(filepath):
    if path.isfile(filepath):
        return [path.abspath(filepath)]
    else:
        dir_list = []
        for root, dirs, files in walk(filepath, topdown=True):
            for file in files:
                dir_list.append(path.join(root, file))
        return dir_list
    

if __name__ == "__main__":
    print(dirList("./data"))

