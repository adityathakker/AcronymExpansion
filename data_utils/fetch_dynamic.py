import os
import wikipedia
from bs4 import BeautifulSoup
import requests
import json
# from config import *
import re
# from get_acronyms import *

DATA_FILE_PATH = "../" + "data/acronyms.json"
#META_FILE_PATH = "../" + META_FILE_PATH
SEARCH_URL = "https://en.wikipedia.org/w/index.php?title=Special:Search&go=Go&search="
DISAMBIGUATION_URL = "https://en.wikipedia.org/wiki/%s_(disambiguation)"

def get_doc(url):
    text = list()
    if url == "":
        #print(url)
        return ""
    response = requests.get(url)
    soup = BeautifulSoup(markup=response.text, features="lxml")
    if soup is None:
        #print(url)
        return ""
    content = soup.find(name="div", attrs={"class": "mw-parser-output"})
    if content is None:
        #print(url)
        return ""
    list_p = content.findAll(name="p")
    if list_p is None:
        #print(url)
        return ""
    for p in list_p:
        text.append(str(p.text))
    return " ".join(text)


def get_pages(query):
    pages = list()
    if len(query.strip()) <= 0:
        raise ValueError

    response = requests.get(SEARCH_URL + str(query))
    soup = BeautifulSoup(markup=response.text, features="lxml")

    if soup is None:
        raise Exception

    if "search" in str(soup.title).lower():
        result_ul = soup.find(name="ul", attrs={"class": "mw-search-results"})
        results_list = result_ul.find_all("li")

        for li in results_list:
            li_div = li.find(name="div", attrs={"class": "mw-search-result-heading"})
            a = li_div.find("a")
            link = "https://en.wikipedia.org" + a["href"]
            heading = str(a.text)
            pages.append((link, heading))

        return pages
    else:
        return wikipedia.summary(query)


def find_full_form(abbr, para):
    re_string = "\\b"
    for c in abbr:
        re_string = re_string + c + "\w+[ _-]"
    re_string = re_string[:len(re_string)-1-4]
    # print(re_string)
    return re.findall(re_string, para)


def check_already_exists(ls, i):
    for x in ls:
        if len(set(x.items()) & set(i.items())) == 2:
            return True
    return False


def get_acronyms(query):
    acronyms = list()

    response = requests.get(DISAMBIGUATION_URL % str(query))
    print(DISAMBIGUATION_URL % str(query))

    query = query.lower()
    if response.status_code != 404:
        print("Disambiguation Page Exists :D")
        soup = BeautifulSoup(markup=response.text, features="lxml")
        if soup is None:
            return None
        div = soup.find("div", attrs={"class": "mw-parser-output"})
        all_uls = div.findAll("ul")

        for ul in all_uls:
            all_lis = ul.findAll("li")
            for li in all_lis:
                a = li.find("a")
                if a is None:
                    continue
                url = "https://en.wikipedia.org" + a["href"]
                content = str(get_doc(url)).lower()
                full_forms = find_full_form(query, content)

                for item in full_forms:
                    print("Item: %s" % item)
                    possible_full_form = dict()
                    possible_full_form["full_form"] = item.strip()
                    possible_full_form["summary"] = content
                    if not check_already_exists(acronyms, possible_full_form):
                        acronyms.append(possible_full_form)
                    else:
                        print("Already Exists")
    if True:
        print("No Disambiguation Page Found. Normally Searching...")
        results = wikipedia.search(query=query, results=10)
        print(results)
        if len(results) <= 0:
            return None

        for each_result in results:
            try:
                summary = str(wikipedia.summary(each_result)).lower()
            except Exception:
                continue
            full_forms = find_full_form(query, summary)

            for item in full_forms:
                print("Item:: %s" % item)
                possible_full_form = dict()
                possible_full_form["full_form"] = item.strip()
                possible_full_form["summary"] = summary
                if not check_already_exists(acronyms, possible_full_form):
                    acronyms.append(possible_full_form)
                else:
                    print("Already Existss")

    return acronyms


def findBestLongForm(shortForm, longForm):
    sIndex = len(shortForm) - 1
    lIndex = len(longForm) - 1
    while sIndex >= 0:
        currChar = shortForm[sIndex].lower()
        if not currChar.isalnum():
            continue

        while (
                    ((lIndex >= 0) and (longForm[lIndex].lower() != currChar))
                or
                    ((sIndex == 0) and (lIndex > 0) and (longForm[lIndex - 1].isalnum()))):
            lIndex -= 1

        if lIndex < 0:
            return None

        lIndex -= 1
        sIndex -= 1

    spIndex = -1
    for c in longForm[lIndex:]:
        if c == " ":
            spIndex = lIndex + 1

        lIndex += 1

    return longForm[:spIndex]



# print(get_acronyms("FDS"))

new_acronyms = dict()
acronyms = json.load(open(DATA_FILE_PATH, mode="r"))
print("Existing File Loaded...")
print("Total Acronyms: %s" % len(acronyms))
i = 1
for item in acronyms:
    print("Acronyms for %s" % item)
    possibilities = get_acronyms(item)
    if possibilities is None or len(possibilities) == 0:
        # del acronyms[item]
        print("No Possibilities :(")
        continue

    acronyms[item]["possibilities"] = possibilities
    # print(possibilities)
    print("%s More to go" % (len(acronyms) - i))
    i += 1
    new_acronyms[item] = acronyms[item]
    print("------------------------------------------------------------")
    if i > 50:
        break
json.dump(new_acronyms, open("../data/new_acronyms.json", "w"))
