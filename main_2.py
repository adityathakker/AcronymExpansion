#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import shuffle
import pprint
import json
import gensim.models
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords

filename = 'data/acronyms_best.json'
f = open(filename, 'r')
data = json.load(f)
stop_words = set(stopwords.words('english'))
n=0
for k,v in data.items():
    n+=1
    print str(n)+"th short form being trained"
    paragraph_list = []
    full_form_list = []
    paragraph_list.append(v["content"][:2000])
    full_form_list.append(v["full_form"])
    for poss in v['possibilities']:
        paragraph_list.append(poss["context"])

        full_form_list.append(poss["full_form"])
    texts = []
    taggeddoc = []
    p_stemmer = PorterStemmer()
    tokeniser = RegexpTokenizer(r'\w+')

    for index, para in enumerate(paragraph_list):
        raw = para.lower()

        tokens = tokeniser.tokenize(raw)
        stopped_tokens = [t for t in tokens if not t in stop_words]

        number_tokens = [x for x in stopped_tokens if x.isalpha]
        stemmed_tokens = [p_stemmer.stem(i) for i in number_tokens]

        length_tokens = [i for i in stemmed_tokens if len(i) > 1]
        texts.append(length_tokens)
        td = TaggedDocument(' '.join(stemmed_tokens).split(), [full_form_list[index]])

        taggeddoc.append(td)
    print("Check 1")
    model = gensim.models.Doc2Vec(taggeddoc, dm=0, alpha=0.025, size=200, min_alpha=0.025, min_count=0)
    print("check 2")
    for epoch in range(12):
        model.train(taggeddoc, total_examples=model.corpus_count, epochs=model.iter)
        model.min_alpha = model.alpha
    print("Done training"+str(n)+"th model")
    model.save('models_context/'+str(k)+'.model')
    print("done saving")

print n

