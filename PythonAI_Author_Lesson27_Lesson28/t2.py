try:  # gensim швидший (код на C), але для Python 3.14 його ще немає
    from gensim.models import KeyedVectors, Word2Vec

    BACKEND = "gensim"
except ImportError:
    from word_vectors import KeyedVectors, Word2Vec

    BACKEND = "numpy"
model = Word2Vec(
    sentences=corpus,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    epochs=100,
    workers=4,
    seed=42,
)
print(model.wv["cat"].shape)  # -> (100,)