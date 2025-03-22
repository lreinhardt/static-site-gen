import os
import shutil
import htmlnode
import sys

def cleanup_directory(root_path):
    if not os.path.exists(root_path):
        return
    
    fs = [os.path.join(root_path, f) for f in os.listdir(root_path)]
    for f in fs:
        if os.path.isfile(f):
            os.unlink(f)
            print(f"removed file: {f}")
        elif os.path.isdir(f):
            cleanup_directory(f)
    
    os.rmdir(root_path)
    print(f"removed directory: {root_path}")


def recursive_copy(src, dst):
    if not os.path.exists(src):
        return
    
    if not os.path.exists(dst):
        os.mkdir(dst)
        print(f"copied directory: {src} to {dst}")

    fs = os.listdir(src)
    for f in fs:
        fsrc = os.path.join(src, f)
        fdst = os.path.join(dst, f)

        if os.path.isfile(fsrc):
            shutil.copy(fsrc, fdst)
            print(f"copied file: {fsrc} to {fdst}")
        elif os.path.isdir(fsrc):
            recursive_copy(fsrc, fdst)


def main():
    cleanup_directory("public")
    recursive_copy("static", "public")

    content_path = "content"
    template_path = "template.html"
    public_path = "public"
    
    htmlnode.generate_pages_recursive(content_path, template_path, public_path)


if __name__ == '__main__':
    main()