#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import gensim
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords


def get_list():
    stop_words = set(stopwords.words('english'))

    filename = 'data/new_acronyms.json'
    f = open(filename, 'r')
    data = json.load(f)
    paragraph_list = []
    full_form_list = []
    for k,v in data.items():
        if k=="WDM":
            for poss in v['possibilities']:
                paragraph_list.append(poss['summary'])
                full_form_list.append(poss['full_form'])
    s="two devices can also function as an add/drop multiplexer (ADM), i.e. simultaneously adding light beams while dropping other light beams and rerouting them to other destinations and devices. Formerly, such filtering of light beams was done with etalons, devices called Fabry–Pérot interferometers using thin-film-coated optical glass. The first WDM technology was conceptualized in the early 1970s and realized in the laboratory in the late 1970s; but these only combined two signals, and many years later were still very expensive.As of 2011, WDM systems can handle 160 signals, which will expand a 10 Gbit/second system with a single fiber optic pair of conductors to more than 1.6 Tbit/second (i.e. 1,600 Gbit/s).Typical WDM systems use single-mode optical fiber (SMF); this is optical fiber for only a single ray of light and having a core diameter of 9 millionths of a meter (9 µm). Other systems with multi-mode fiber cables (MM Fiber; also called premises cables) have core diameters of about 50 µm. Standardization and extensive research have brought down system costs significantly."
    paragraph_list.append(s)
    full_form_list.append("Wavelength context")
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

    return taggeddoc
