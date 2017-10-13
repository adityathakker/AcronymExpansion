import gensim.models
print("Start")

from main_2 import get_list

print("Check 1")
taggeddoc = get_list()
print("check 1.5")
model = gensim.models.Doc2Vec(taggeddoc, dm = 0, alpha=0.025, size= 20, min_alpha=0.025, min_count=0)
print("check 2")
for epoch in range(1):
    print('Now training epoch %s'%epoch)
    model.train(taggeddoc, total_examples=model.corpus_count, epochs=model.iter)
    model.alpha -= 0.002
    model.min_alpha = model.alpha
print("Done training")
model.save('trained_2.model')
print("done saving")