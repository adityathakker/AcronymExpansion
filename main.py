import json
import gensim
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.models.doc2vec import TaggedDocument
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

filename = 'data/acronyms.json'
f = open(filename, 'r')
data = json.load(f)
paragraph_list = []
full_form_list = []
for k,v in data.items():
    paragraph_list.append(v["content"])
    full_form_list.append(v["full_form"])
texts = []
taggeddoc = []

p_stemmer = PorterStemmer()
tokeniser = RegexpTokenizer(r'\w+')

for index,para in enumerate(paragraph_list):


    raw = para.lower()

    tokens = tokeniser.tokenize(raw)
    stopped_tokens = [t for t in tokens if not t in stop_words]
    number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
    number_tokens = ' '.join(number_tokens).split()
    stemmed_tokens = [p_stemmer.stem(i) for i in number_tokens]
    length_tokens = [i for i in stemmed_tokens if len(i) > 1]
    texts.append(length_tokens)

    td = TaggedDocument(gensim.utils.to_unicode(' '.join(stemmed_tokens)).split(),str(index))
    taggeddoc.append(td)





