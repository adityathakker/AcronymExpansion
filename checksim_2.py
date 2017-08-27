import json
import gensim.models
from difflib import SequenceMatcher

filename = 'data/acronyms_best.json'
f = open(filename, 'r')
data = json.load(f)
model = gensim.models.Doc2Vec.load('models_context/IC.model')
#print model.docvecs.similarity("Entity-Relationship Model","entity-relationship models")
print model.docvecs.most_similar("Integrated Circuit",topn=20)
#
total =0
correct=0
error=0
def similar(a, b):
    a=a.lower()
    b=b.lower()
    return SequenceMatcher(None, a, b).ratio()
n=0
wrong =0
for k,v in data.items():
    try:
        model = gensim.models.Doc2Vec.load('models_context/'+k+'.model')
        if similar(v["full_form"],model.docvecs.most_similar(v["full_form"])[0][0])>0.80:
            correct+=1
        else:
            print v["full_form"]+" : "+str(model.docvecs.most_similar(v["full_form"])[0])
            wrong +=1

        total+=1
    except KeyError:
        error+=1
    except IndexError:
        error+=1
    n+=1
print n
print "Accuracy is"+str(float(correct)/float(total))
print "errors are : " +str(error)
print wrong
print correct



