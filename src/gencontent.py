import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("markdown is not header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_data = f.read()
    with open(template_path, "r") as f:
        template_data = f.read()

    markdown_data_html = markdown_to_html_node(markdown_data).to_html()
    title_page = extract_title(markdown_data)

    template_data = template_data.replace("{{ Title }}", title_page)
    template_data = template_data.replace("{{ Content }}", markdown_data_html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(template_data)

def generate_page_recursive(from_path, template_path, dest_path):
    for path in os.listdir(from_path):
        full_path = os.path.join(from_path, path)
        full_dest_path = os.path.join(dest_path, path)
        if os.path.isdir(full_path) == True:
            generate_page_recursive(full_path, template_path, full_dest_path)
        else:
            if path.endswith(".md"):
                final = full_dest_path.replace(".md", ".html")
                generate_page(full_path, template_path, final)

    
    