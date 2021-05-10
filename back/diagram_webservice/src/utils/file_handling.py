from .aliases import OUT_DIR
import os

# Control all images file extensions.
IMAGE_FORMAT = ".png"

# _ in file name will be kept to specify, that it's a generated image
def generate_file_name(*args):
    file_name = ""
    for arg in args:
        file_name = f"{file_name}_{str(arg)}"
    return file_name

def file_name_exists(file_name):
    return os.path.isfile(f"{OUT_DIR}/{file_name}{IMAGE_FORMAT}")