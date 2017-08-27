import os
import wikipedia
from bs4 import BeautifulSoup
import requests
import json
import re

DATA_FILE_PATH = "../" + "data/acronyms.json"
SEARCH_URL = "https://en.wikipedia.org/w/index.php?title=Special:Search&go=Go&search="
DISAMBIGUATION_URL = "https://en.wikipedia.org/wiki/%s_(disambiguation)"


def get_doc(url):
    text_all = list()
    if url == "":
        # print(url)
        return ""
    response = requests.get(url)
    soup = BeautifulSoup(markup=response.text, features="lxml")
    if soup is None:
        # print(url)
        return ""
    content = soup.find(name="div", attrs={"class": "mw-parser-output"})
    if content is None:
        # print(url)
        return ""
    list_p = content.findAll(name="p")
    if list_p is None:
        # print(url)
        return ""

    for p in list_p:
        text_all.append(str(p.text))
    return " ".join(text_all)


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
    re_string = re_string[:len(re_string) - 1 - 4]
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
                    context_ix = content.find(item)
                    if context_ix == -1:
                        continue
                    if (500 - context_ix) >= 0:
                        start = 0
                    else:
                        start = context_ix - 500
                    if (len(content) - context_ix) >= 500:
                        end = context_ix + 500
                    else:
                        end = len(content) - context_ix
                    possible_full_form["context"] = content[start:end]
                    possible_full_form["source"] = content
                    # print(possible_full_form)
                    if not check_already_exists(acronyms, possible_full_form):
                        acronyms.append(possible_full_form)
                    else:
                        print("Already Exists")

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
            context_ix = summary.find(item)
            if context_ix == -1:
                continue
            if (500 - context_ix) >= 0:
                start = 0
            else:
                start = context_ix - 500
            if (len(summary) - context_ix) >= 500:
                end = context_ix + 500
            else:
                end = len(summary) - context_ix
            possible_full_form["context"] = summary[start:end]
            possible_full_form["source"] = summary
            if not check_already_exists(acronyms, possible_full_form):
                acronyms.append(possible_full_form)
            else:
                print("Already Exists")

    return acronyms


# print(get_acronyms("FDS"))

new_acronyms = dict()
acronyms = json.load(open(DATA_FILE_PATH, mode="r"))
print("Existing File Loaded...")
print("Total Acronyms: %s" % len(acronyms))
i = 1
for item in acronyms:
    print("Acronyms for %s" % item)
    # get_acronyms(item)
    try:
        possibilities = get_acronyms(item)
    except Exception as e:

        print(e)
        print("Exception Occurred")
        continue
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
json.dump(new_acronyms, open("../data/new_acronyms.json", "w"))
