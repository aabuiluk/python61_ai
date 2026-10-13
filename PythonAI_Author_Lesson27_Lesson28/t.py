sentences = [
    "the cat drinks milk",
    "the dog drinks water",
    "the cat likes the dog"
]

corpus = [sentence.lower().split() for sentence in sentences]
print(corpus)
# [['the', 'cat', 'drinks', 'milk'],
#  ['the', 'dog', 'drinks', 'water'],
#  ['the', 'cat', 'likes', 'the', 'dog']]

vocabulary = sorted({word for sentence in corpus for word in sentence})
print(vocabulary)
# ['cat', 'dog', 'drinks', 'likes', 'milk', 'the', 'water']


cat = [ 0.72,  0.14, -0.31, 0.11]
dog = [ 0.68,  0.19, -0.28, 0.11]
car = [-0.11,  0.81,  0.54, 0.11]

import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

cat = [1.0, 0.2]
dog = [0.9, 0.3]
car = [0.1, 1.0]

print(cosine(cat, dog))
print(cosine(cat, car))