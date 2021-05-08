from .aliases import OUT_DIR
import os

# _ in file name will be kept to specify, that it's a generated image
def generate_file_name(*args):
    file_name = ""
    for arg in args:
        file_name = f"{file_name}_{str(arg)}"
    if os.path.isfile(f"{OUT_DIR}/{file_name}"):
        return False
    else:
        return file_name
