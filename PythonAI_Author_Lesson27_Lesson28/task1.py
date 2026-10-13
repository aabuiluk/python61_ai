try:  # gensim швидший (код на C), але для Python 3.14 його ще немає
    from gensim.models import KeyedVectors, Word2Vec

    BACKEND = "gensim"
except ImportError:
    from word_vectors import KeyedVectors, Word2Vec


texts = [
    "cat drinks milk",
    "dog drinks water",
    "cat and dog are animals",
    "kitten is a young cat",
    "puppy is a young dog",
    "animals need food and water",
    "cat likes warm milk",
    "dog likes long walks"
]

corpus = [text.lower().split() for text in texts]

model = Word2Vec(
    sentences=corpus,
    vector_size=50,
    window=2,
    min_count=1,
    sg=1,
    epochs=300,
    seed=42
)

print("Vocabulary:", list(model.wv.index_to_key))
print("cat vector shape:", model.wv["cat"].shape)
print("cat-dog:", model.wv.similarity("cat", "dog"))
print("cat-milk:", model.wv.similarity("cat", "milk"))
print("Nearest to cat:", model.wv.most_similar("cat", topn=5))