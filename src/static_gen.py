import os
import shutil
import re
from pathlib import Path
from block import markdown_to_html_node

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

def extract_title(markdown):
    if re.match(r"^# .+", markdown):
        return markdown[2:]
    raise ValueError("No h1 header")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
        
    title = extract_title(markdown)
    hnode = markdown_to_html_node(markdown)
    content = hnode.to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
#    template = template.replace('href="/', f'href="{basepath}')
#    template = template.replace('src="/', f'src="{basepath}')
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_path = Path(dir_path_content)
    if not content_path.exists():
        raise ValueError(f"Directory does not exist: {dir_path_content}")
    elif not content_path.is_dir():
        raise ValueError(f"Path is not a directory: {dir_path_content}")

    for md_file in content_path.rglob("*.md"):
        rel_path = md_file.relative_to(content_path)
        final_path = str(rel_path).replace(".md", ".html")
        generate_page(md_file, template_path, (dest_dir_path + "/" + final_path), basepath)
