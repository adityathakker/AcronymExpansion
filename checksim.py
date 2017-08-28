<<<<<<< HEAD
import gensim
print("start")
model = gensim.models.Doc2Vec.load('trained_2.model')

print(model.docvecs.most_similar('Wavelength context'))
=======
import wikipedia
# print("start")
# model = gensim.models.Doc2Vec.load('trained.model')
#
# print(model.docvecs.most_similar('Cryptography Next Generation'))

print wikipedia.suggest("IC")
>>>>>>> 08e18fa3d90f73094e36262c6dcbc87b6c8b71c8
