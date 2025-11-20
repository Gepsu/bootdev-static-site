import os
import re
import shutil

from src.markdown_blocks import markdown_to_html


def main() -> None:
    clean_public_directory()
    copy_contents("./static", "./public")
    generate_pages("./content", "./public", "./template.html")


def clean_public_directory() -> None:
    if os.path.exists("./public"):
        shutil.rmtree("./public")


def copy_contents(src: str, dest: str) -> None:
    contents = get_contents_r(src)
    for item in contents:
        src_file = os.path.join(src, item)
        dest_file = os.path.join(dest, item)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy(src_file, dest_file)


def generate_pages(src: str, dest: str, template: str) -> None:
    pages = get_contents_r(src)
    for page in pages:
        if not page.endswith(".md"):
            continue
        src_page = os.path.join(src, page)
        dest_page = os.path.join(dest, page.replace(".md", ".html"))
        os.makedirs(os.path.dirname(dest_page), exist_ok=True)
        generate_page(src_page, dest_page, template)


def get_contents_r(dir: str, root: str = "") -> list[str]:
    if not root:
        root = dir

    paths = []

    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
        if os.path.isfile(item_path):
            paths.append(os.path.relpath(item_path, root))
        elif os.path.isdir(item_path):
            paths.extend(get_contents_r(item_path, root))

    return paths


def extract_title(markdown: str) -> str:
    match = re.match(r"^#\s(.*)", markdown.strip())
    if not match:
        raise ValueError("No title header found")
    return match[1]


def generate_page(src: str, dest: str, template: str) -> None:
    print(f"Generating page from {src} to {dest} using {template}")

    with open(src) as file:
        source_contents = file.read()

    with open(template) as file:
        template_contents = file.read()

    markdown = markdown_to_html(source_contents)
    title = extract_title(source_contents)

    html = template_contents.replace("{{ Title }}", title).replace(
        "{{ Content }}", markdown.to_html()
    )

    with open(dest, "w") as file:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        file.write(html)


if __name__ == "__main__":
    main()
