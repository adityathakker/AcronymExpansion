import gensim
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

print "imported"
model = gensim.models.Doc2Vec.load('trained.model')
docvecs = model.docvecs
print "check 1"
print docvecs.count