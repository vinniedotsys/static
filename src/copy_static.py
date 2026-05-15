import os
import shutil

def generate_public_dir():
    src = "./static"
    dst = "./public"

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    def _copy_contents(current_src, current_dst):
        for name in os.listdir(current_src):
            src_path = os.path.join(current_src, name)
            dst_path = os.path.join(current_dst, name)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
            else:
                os.mkdir(dst_path)
                _copy_contents(src_path, dst_path)

    _copy_contents(src, dst)

