import gensim
print "start"
model = gensim.models.Doc2Vec.load('trained.model')

print model.docvecs.most_similar('Computational Fluid Dynamics')
