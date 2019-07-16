import os

def get_par_files():
    root_dir = os.getcwd()
    for subdirs, dirs, files in os.walk(root_dir):
        print(subdirs, '\n')
        print(dirs, '\n')
