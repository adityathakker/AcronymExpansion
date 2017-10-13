
import json
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer



def search(k,x):
    count=0
    for y in data[k]["possibilities"]:
        if y["full_form"]==x and count>0:
            return True
        elif y["full_form"]==x:
            count+=1
    return False

def similar(a, b):
    a=a.lower()
    b=b.lower()
    return SequenceMatcher(None, a, b).ratio()

filename = 'data/acronyms_best.json'
f = open(filename, 'r+')
data = json.load(f)

################################
# kept = 0
# removed =0
# for k,v in data.items():
#     for poss in v["possibilities"]:
#         if search(k,poss["full_form"]):
#             v["possibilities"].remove(poss)
#             print "Removed : "+poss["full_form"]
#             removed+=1
#         else:
#             print "Kept : " +poss["full_form"]
#             kept+=1
# print kept
# print removed

###############################
# ns=0
# for k,v in data.items():
#
#     flag=0
#     for poss in v["possibilities"]:
#         rat = similar(v["full_form"], poss["full_form"])
#         if rat>=0.8:
#             flag=1
#             break
#     if flag==0:
#         ns+=1
#         del data[k]
#
# print "not similar :"+str(ns)
###############################
stop_words = set(stopwords.words('english'))
tokeniser = RegexpTokenizer(r'\w+')
count1=0
count2=0
count3=0
for k,v in data.items():
    if len(tokeniser.tokenize(v["full_form"].lower()))<2:
        print "Removing "+k
        del data[k]
    try:
        for a in tokeniser.tokenize(v["full_form"].lower()):
            if a in stop_words:
                print "RRemoving "+v["full_form"]
                del data[k]
    except KeyError:
        pass
        for poss in v["possibilities"]:
            try:
                for b in tokeniser.tokenize(poss["full_form"]):
                    if b in stop_words:
                        print "removing " + poss["full_form"]
                        v["possibilities"].remove(poss)
            except ValueError:
                print "Error"
                pass








#
with open('data/acronyms_best.json', 'w') as outfile:
    json.dump(data, outfile)