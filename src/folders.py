import os

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def create(folders: list):
    for folder in folders:
        create_folder(folder)