from bs4 import BeautifulSoup
import requests
import json
from config import *

DATA_FILE_PATH = "../" + DATA_FILE_PATH
MAIN_URL = "https://en.wikipedia.org/wiki/List_of_computing_and_IT_abbreviations"


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
acronyms = dict()

r = requests.get(MAIN_URL)
bs = BeautifulSoup(markup=r.text, features="lxml")

all_li = bs.find_all("li")
print("Total Acronyms: %s" % len(all_li))
i = 1
for li in all_li:
    txt = str(li.text)
    if "—" in txt:
        try:
            link = "https://en.wikipedia.org" + str(li.a["href"])
        except Exception as e:
            link = ""
        tmp = txt.split("—")
        abbr = tmp[0]
        full_form = tmp[1]
        content = get_doc(link)

        acronyms[abbr] = dict()
        acronyms[abbr]["link"] = link
        acronyms[abbr]["full_form"] = full_form
        acronyms[abbr]["content"] = content
        print("Processed %s of %s" % (i, len(all_li)))
        i += 1

print(acronyms)
with open(DATA_FILE_PATH, mode="w", encoding="utf-8") as file:
    json.dump(acronyms, file)
