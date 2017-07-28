import os

from bs4 import BeautifulSoup
import requests
import json
from config import *

DATA_FILE_PATH = "../" + DATA_FILE_PATH
META_FILE_PATH = "../" + META_FILE_PATH
MAIN_URL = "https://en.wikipedia.org/wiki/List_of_computing_and_IT_abbreviations"


def save_json(obj, i):
    with open(META_FILE_PATH, mode="w", encoding="utf-8") as file:
        json.dump({"last_key": i}, file)

    with open(DATA_FILE_PATH, mode="w", encoding="utf-8") as file:
        json.dump(obj, file)


def get_doc(url):
    text = list()
    if url == "":
        print(url)
        return ""
    response = requests.get(url)
    soup = BeautifulSoup(markup=response.text, features="lxml")
    if soup is None:
        print(url)
        return ""
    content = soup.find(name="div", attrs={"class": "mw-parser-output"})
    if content is None:
        print(url)
        return ""
    list_p = content.findAll(name="p")
    if list_p is None:
        print(url)
        return ""
    for p in list_p:
        text.append(str(p.text))
    return " ".join(text)

# to store all the acronyms
if os.path.exists(DATA_FILE_PATH):
    acronyms = json.load(open(DATA_FILE_PATH, "r", encoding="utf-8"))
else:
    acronyms = dict()

if os.path.exists(META_FILE_PATH):
    meta = json.load(open(META_FILE_PATH, "r", encoding="utf-8"))
    i = meta["last_key"] + 1
else:
    i = 0

r = requests.get(MAIN_URL)
bs = BeautifulSoup(markup=r.text, features="lxml")

all_li = bs.find_all("li")
print("Total Acronyms: %s" % len(all_li))
print("Continuing where left...") if i > 1 else 0
for li in all_li[i:]:
    txt = str(li.text)
    if "—" in txt:
        try:
            link = "https://en.wikipedia.org" + str(li.a["href"])
        except Exception as e:
            link = ""
        tmp = txt.split("—")
        abbr = tmp[0]
        full_form = tmp[1]
        try:
            content = get_doc(link)
        except Exception:
            save_json(acronyms, i)
        acronyms[abbr] = dict()
        acronyms[abbr]["link"] = link
        acronyms[abbr]["full_form"] = full_form
        acronyms[abbr]["content"] = content
        print("Processed %s of %s" % (i, len(all_li)))
        i += 1

print(acronyms)
save_json(acronyms, i)
