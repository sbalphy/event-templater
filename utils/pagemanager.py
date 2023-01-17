
import sys
import os
import json
import re
from jinja2 import Environment, FileSystemLoader

def createpage(pages, name):
    pages.append(name)
    updateall(pages)
    print(f"Page {name}.html created and navigation bars updated.")
    return


def updatepage(pages, name):
    filename = f"{name}.html"
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("template.html")
    originalcontent = fetchcontent(f"../content/{filename}")
    content = template.render(
        name = name,
        pages = pages,
        originalcontent = originalcontent
    )
    with open(f"../content/{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Page {filename} updated.")
    return

def fetchcontent(path):
    try:
        with open(path, mode="r", encoding="utf-8") as page:
            data = page.read() 
            regex = r"<!--content-->((.|\n)*?)<!--content-->"
            return re.search(regex, data).group(1)
    except FileNotFoundError:
        return None

def updateall(pages):
    for page in pages:
        updatepage(pages, page)
    print(f"Updated all pages.")

def removepage(pages, name):
    filename = f"{name}.html"
    check = input(f"Deleting page {filename}. Are you sure? (y/N) ")
    if check == "y" or check == "Y":
        os.remove(f"../content/{filename}")
        pages.remove(name)
        print(f"Page {filename} removed.")
        updateall(pages)
        print("Navigation bars updated.")
    else:
        print("Aborting deletion.")

def main():
    command = sys.argv[1]
    try:
        name = sys.argv[2]
    except IndexError:
        name = None
        print("No file name given. Hopefully you're running update-all.")
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