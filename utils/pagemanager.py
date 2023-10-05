
import sys
import os
import json
import re
from jinja2 import Environment, FileSystemLoader

def createpage(pages, name):
    print(f"Reading info from info/{name} file.")
    try:
        with open(f"info/{name}", mode="r", encoding="utf-8") as f:
            info = f.read().split(';')
            title = info[0]
            intro = info[1]
            sections = [tuple(item.split('\n')) for item in info[2].split(',')]
            students = [tuple(item.split('\n')) for item in info[3].split(',')]
    except FileNotFoundError:
        print(f"File info/{name} was not found. Aborting page creation.")
        return      
    pages[name] = title
    print(f"Creating {name} folder.")
    os.mkdir(f"../{name}")
    os.mkdir(f"../{name}/images")
    print(f"Writing template to {name}/index.html.")
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("new-page.html.j2")
    content = template.render(
        title = title,
        pages = pages.keys(),
        intro = intro
        sections = sections
        students = students
    )
    with open(f"../{name}/index.html", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Page {name}/index.html created. Updating navigation bars.")
    updateall(pages)
    print(f"Navigation bars updated. Page creation has been successful.")
    return


def updatepage(pages, name):
    filename = f"{name}/index.html"
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("update-page.html.j2")
    originalcontent = fetchcontent(f"../{filename}")
    content = template.render(
        title = pages[name],
        pages = pages.keys(),
        originalcontent = originalcontent
    )
    with open(f"../{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Page {filename} updated.")
    return

def updateroot(pages):
    filename = "index.html"
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("update-root.html.j2")
    originalcontent = fetchcontent(f"../{filename}")
    content = template.render(
        pages = pages.keys(),
        originalcontent = originalcontent
    )
    with open(f"../{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Root index updated.")
    return


def fetchcontent(path):
    try:
        with open(path, mode="r", encoding="utf-8") as page:
            data = page.read() 
            regex = r"<!--content-->((.|\n)*?)<!--content-->"
            return re.search(regex, data).group(1)
    except FileNotFoundError:
        print(f"File {path} was not found.")
        return None

def updateall(pages):
    updateroot(pages)
    print(f"Updated index page.")
    for page in pages:
        updatepage(pages, page)
    print(f"Updated all pages.")
    return

def removepage(pages, name):
    filename = f"{name}/index.html"
    check = input(f"Deleting page {filename}. Are you sure? This will not delete the whole directory. (y/N) ")
    if check == "y" or check == "Y":
        os.remove(f"../{filename}")
        pages.pop(name)
        print(f"Page {filename} removed.")
        updateall(pages)
        print("Navigation bars updated.")
    else:
        print("Aborting deletion.")
    return

def main():
    command = sys.argv[1]
    try:
        name = sys.argv[2]
    except IndexError:
        name = None
        print("No page name given. Hopefully you're running update-all.")
    with open("./pages.json", "r") as f:
        pages = json.load(f)
    if command == "create":
        createpage(pages, name)
    elif command == "remove":
        removepage(pages, name)
    elif command == "update":
        updatepage(pages, name)
    elif command == "update-all":
        updateall(pages)
    else:
        print(f"Unidentified command {command}. Nothing has been updated.")
    with open("./pages.json", "w") as f:   
        json.dump(pages, f, indent=1)

if __name__ == "__main__":
    main()