import os


def my_rename(pathname):
    dirlist = os.listdir(pathname)
    for path in dirlist:
        if '.' in path:
            oddname = os.path.join(pathname, path)
            newname = str(pathname) + str(path)
            os.rename(oddname, newname)
        else:
            my_rename(os.path.join(pathname, path))



if __name__ == '__main__':
    # my_rename('images/set07')
    # print('1')
    my_rename(r'H:\data2\groundtruth')
    # print('2')
    # my_rename(r'H:\homework_data\annotations')
    print('3')
    # my_rename('annotations')
    print('4')
    # my_rename('new_add')
