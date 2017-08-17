import gensim
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
print("start")
model = gensim.models.Doc2Vec.load('trained.model')
print("check 1")
X = model[model.wv.vocab]
print("check 2")
tsne = TSNE(n_components=2)
print("check 3")
X_tsne = tsne.fit_transform(X)
print("check 4")
plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
print("check 5")
plt.show()
print("done")