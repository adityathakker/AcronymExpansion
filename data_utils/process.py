import json
from config import *

DATA_FILE_PATH = "../" + DATA_FILE_PATH
with open(DATA_FILE_PATH, mode="r", encoding="utf-8") as file:
    acronyms = json.load(file)
    len(acronyms)