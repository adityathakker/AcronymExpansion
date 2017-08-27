import gensim
print("start")
model = gensim.models.Doc2Vec.load('trained_2.model')

print(model.docvecs.most_similar('Wavelength context'))
