from textnode import TextNode, TextType
from copystatic import copy_directory_recursive
import os

def main():
    source_dir = "static"
    dest_dir = "public"
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist. Please create it and add some files.")
        return

    print("Starting copy process...")
    copy_directory_recursive(source_dir, dest_dir)


main()
