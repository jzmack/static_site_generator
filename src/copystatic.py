import os
import shutil

def copy_directory_recursive(src, dest):

    if os.path.exists(dest):
        print(f"Deleting existing destination directory: {dest}")
        shutil.rmtree(dest)

    os.mkdir(dest)
    print(f"Created destination directory: {dest}")

    def recursive_copy(src_path, dest_path):
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)

            if os.path.isfile(src_item):
                shutil.copy(src_item, dest_item)
                print(f"Copied file: {src_item} -> {dest_item}")
            else:
                os.mkdir(dest_item)
                print(f"Created directory: {dest_item}")
                recursive_copy(src_item, dest_item)

    recursive_copy(src, dest)

