import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page, generate_page_recursive



def main():
    source = "static"
    destination = "public"

    print("Cleaning destination directory...")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    print(f"Copying files from {source} to {destination}...")
    copy_files_recursive(source, destination)

    generate_page_recursive("content", "template.html", "public")
    
main()