import json

DATA_FILE_PATH = "../" + "data/biggest.json"
ABBR_LIST = "../" + "data/list_of_abbr"

i = 1
with open(DATA_FILE_PATH, mode="r", encoding="utf-8") as file:
    acronyms = json.load(file)
    new_acronyms = dict()
    with open(ABBR_LIST, mode="r", encoding="utf-8") as abbr_file:
        print("processing %s" % i)
        i += 1
        for abbr in abbr_file:
            new_acronyms[abbr] = acronyms[abbr]
            ix = str(new_acronyms[abbr]["content"]).lower().rfind(str(abbr).lower())
            length = len(new_acronyms[abbr]["content"])
            if ix > 1000:
                start = ix - 1000
            else:
                start = 0

            if length - ix > 1000:
                end = ix + 1000
            else:
                end = length
            new_acronyms[abbr]["context"] = new_acronyms[abbr]["content"][start:end]

            new_poss = list()
            for i in new_acronyms[abbr]["possibilities"]:
                i["content"] = i.pop("source")
                new_poss.append(i)
            new_acronyms[abbr]["possibilities"] = new_poss

json.dump(new_acronyms, open("../data/new_acronyms.json", mode="w", encoding="utf-8"))
