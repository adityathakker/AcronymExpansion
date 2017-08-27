<<<<<<< HEAD
import wikipedia
# print("start")
# model = gensim.models.Doc2Vec.load('trained.model')
#
# print(model.docvecs.most_similar('Cryptography Next Generation'))

print wikipedia.suggest("IC")
=======
import gensim
print("start")
model = gensim.models.Doc2Vec.load('trained_2.model')

print(model.docvecs.most_similar('Wavelength context'))
>>>>>>> a3118e1c210425395bfd41407f527b4540a7c3bc
