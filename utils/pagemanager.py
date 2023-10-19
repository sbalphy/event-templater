
import sys
import os
import json
import re
import csv
from jinja2 import Environment, FileSystemLoader

def parsecsv(pages, filename):
    print(f"Parsing file {filename}...")
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            page = row[1].lower()
            if page in pages:
                check = input(f"Page {page} already exists in pagelist. Overwrite? (y/N) ")
                if check.lower() != "y":
                    print(f"Page {page} has been skipped.")
                    continue
            print(f"Adding {page} entry to pagelist.")
            pages[page] = {
                'title': row[2],
                'description': row[3],
                'intro': row[5],
                'sections': [list(pair) for pair in zip(row[6:14:2], row[7:14:2])],
                'students': [[student.split(' ')[0].lower(), student] for student in row[14:19]],
                'links': [list(pair) for pair in zip(row[21:30:2], row[20:30:2])]
                }
    return

def createpage(pages, name):
    print(f"Creating page {name}, based on the information in pages.json.")
    if name not in pages:
        print(f"Page {name} not found in pages.json. Try running 'pagemanager.py parse' first.")
        return
    print(f"Creating {name} folder.")
    os.mkdir(f"../content/{name}")
    os.mkdir(f"../content/{name}/images")
    generatepage(pages, name)
    print(f"Page {name}/index.html created. Updating navigation bars.")
    updateall(pages)
    print(f"Navigation bars updated. Page creation has been successful.")
    return

def generatepage(pages, name):
    page = pages[name]
    print(f"Writing new page template to {name}/index.html.")
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("new-page.html.j2")
    content = template.render(
        title = page['title'],
        pages = pages.keys(),
        intro = page['intro'],
        sections = page['sections'],
        links = page['links'],
        students = page['students']
    )
    with open(f"../content/{name}/index.html", mode="w", encoding="utf-8") as target:
        target.write(content)
    print(f"Page {name}/index.html generated.")
    return

def regenerateall(pages, name):
    print(f"Regenerating all pages from pages.json info.")
    for page in pages:
        check = input(f"Regenerating {page}, are you sure? (y/N)")
        if check.lower() != 'y':
            print(f"Skipping {page}")
            continue
        generatepage(pages, page)
    print(f"Regenerated every page.")
    return

def updatepage(pages, name):
    filename = f"content/{name}/index.html"
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("update-page.html.j2")
    originalcontent = fetchcontent(f"../{filename}")
    content = template.render(
        title = pages[name]["title"],
        pages = pages.keys(),
        originalcontent = originalcontent
    )
    with open(f"../{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Page {filename} updated.")
    return

def updateroot(pages):
    filename = "content/index.html"
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("update-root.html.j2")
    originalcontent = fetchcontent(f"../{filename}")
    pageinfo = [(name, values['title'], values['description']) for name, values in pages.items()]
    content = template.render(
        pages = pages.keys(),
        originalcontent = originalcontent,
        pageinfo = pageinfo
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
    filename = f"content/{name}/index.html"
    check = input(f"Deleting page {filename}. Are you sure? This will not delete the whole directory. (y/N) ")
    if check.lower() == "y":
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
    elif command == "regenerate":
        generatepage(pages, name)
    elif command == "regenerate-all":
        regenerateall(pages, name)
    elif command == "parse":
        parsecsv(pages, "answers.csv")
    else:
        print(f"Unidentified command {command}. Nothing has been updated.")
    with open("./pages.json", "w") as f:   
        json.dump(pages, f, indent=1)

if __name__ == "__main__":
    main()
