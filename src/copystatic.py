import os
import shutil

def copy_files_recursive(src_path, dst_path):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    # List everything in the source directory
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dst_item = os.path.join(dst_path, item)

        print(f" * {src_item} -> {dst_item}")

        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_item)
        else:
            # It's a directory, let's go deeper!
            copy_files_recursive(src_item, dst_item)