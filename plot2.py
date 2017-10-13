import gensim
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

print("imported")
model = gensim.models.Doc2Vec.load('trained.model')
docvecs = model.docvecs
print("check 1")
doc_labels = []
doc_vecs = []
for k in docvecs.doctags.keys():
    doc_labels.append(k)
    print(k)
    doc_vecs.append(docvecs[k])
print("check 2")
pca = PCA(n_components=2)
pca.fit(doc_vecs)
print("check 3")
reduced = pca.transform(doc_vecs)
print("check 4")
for index, vec in enumerate(reduced):
    print('%s %s' % (doc_labels[index], vec))
    if index < 1400:
        x, y = vec[0], vec[1]
        plt.scatter(x, y)
        plt.annotate(doc_labels[index], xy=(x, y))

print("check 5")
plt.show()
print("done")
