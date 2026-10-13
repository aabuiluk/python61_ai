texts = ["cat drinks milk",
         "dog drinks water"]
tokens = [s.lower().split() for s in texts]
vocab = {"<PAD>": 0, "<UNK>": 1}
for sent in tokens:
    for word in sent:
        if word not in vocab:
            vocab[word] = len(vocab)

def encode(sentence, max_len=5):
    ids = [vocab.get(w, vocab["<UNK>"]) for w in sentence.lower().split()]
    return (ids[:max_len] + [vocab["<PAD>"]] * max(0, max_len-len(ids)))

print(vocab)
print(encode("cat drinks juice"))
print(encode("dog drinks hot water"))