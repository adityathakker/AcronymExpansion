import os
import wikipedia
from bs4 import BeautifulSoup
import requests
import json
from config import *
import re
from data_utils.get_acronyms import *

DATA_FILE_PATH = "../" + DATA_FILE_PATH
META_FILE_PATH = "../" + META_FILE_PATH
SEARCH_URL = "https://en.wikipedia.org/w/index.php?title=Special:Search&go=Go&search="
DISAMBIGUATION_URL = "https://en.wikipedia.org/wiki/%s_(disambiguation)"


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
    re_string = ""
    for c in abbr:
        re_string = re_string + c + "\w+ "
    return re.findall(re_string, para)


def get_acronyms(query):
    acronyms = list()
    query = query.lower()

    response = requests.get(DISAMBIGUATION_URL % str(query))
    if response.status_code != 404:
        print("Disambiguation Page Exists :D")
        soup = BeautifulSoup(markup=response.text, features="lxml")
        if soup is None:
            return None
        div = soup.find("div", attrs={"class": "mw-content-text"})
        all_uls = div.find_all("ul")

        for ul in all_uls:
            all_lis = ul.find_all("li")
            for li in all_lis:
                a = li.find("a")
                url = "https://en.wikipedia.org" + a["href"]
                content = get_doc(url)
                full_forms = find_full_form(query, content)

                for item in full_forms:
                    print(item)
                    possible_full_form = dict()
                    possible_full_form["full_form"] = item.strip()
                    possible_full_form["summary"] = content
                    acronyms.append(possible_full_form)
    else:
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
                print(item)
                possible_full_form = dict()
                possible_full_form["full_form"] = item.strip()
                possible_full_form["summary"] = summary
                acronyms.append(possible_full_form)

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


acronyms = json.load(open(DATA_FILE_PATH, mode="r"))
print("Existing File Loaded...")
print("Total Acronyms: %s" % len(acronyms))
i = 1
for item in acronyms:
    print("Acronyms for %s" % item)
    possibilities = get_acronyms(item)
    if possibilities is None or len(possibilities) == 0:
        del acronyms[item]
        continue

    acronyms[item]["possibilities"] = possibilities
    print(possibilities)
    print("%s More to go" % (len(acronyms) - i))
    i += 1
    print()
