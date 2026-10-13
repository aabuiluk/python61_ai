# text = "The movies were Not really good, but the actors were amazing and not bad! "
# text = text.lower()
#
# from nltk.tokenize import word_tokenize
#
# tokens = word_tokenize(text)
# print(tokens)
#
# print(text.split())
#
# words = [token for token in tokens if token.isalpha()]
# print(words)
#
# from nltk.corpus import stopwords
#
# stop_words = set(stopwords.words("english"))
# stop_words.discard("not")
# filtered = [
#     word for word in words
#     if word not in stop_words
# ]
# print(filtered)
#
# print(stopwords.words("english"))
#
# from nltk.stem import PorterStemmer
#
# stemmer = PorterStemmer()
#
# for word in ["connect", "connected", "connecting", "connection"]:
#     print(word, "->", stemmer.stem(word))
#
# print(stemmer.stem("charging"))
#
#
# from nltk.stem import WordNetLemmatizer
#
# lemmatizer = WordNetLemmatizer()
#
# print(lemmatizer.lemmatize("cars"))
# print(lemmatizer.lemmatize("studies"))
# print(lemmatizer.lemmatize("charging"))

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

text = "The movies were Not really good, but the actors were amazing and not bad! "

# 1. Нормалізуємо register
text = text.lower()

# 2. Розбиваємо text на tokens
tokens = word_tokenize(text)

# 3. Беремо stop-word list
stop_words = set(stopwords.words("english"))

# 4. Для sentiment залишаємо negation
stop_words.discard("not")

# 5. Залишаємо alphabetic tokens і прибираємо stop words
filtered = [
    token
    for token in tokens
    if token.isalpha() and token not in stop_words
]

# 6. Lemmatization
lemmatizer = WordNetLemmatizer()

lemmas = [
    lemmatizer.lemmatize(token)
    for token in filtered
]

print("Original:", text)
print("Tokens:", tokens)
print("Filtered:", filtered)
print("Lemmas:", lemmas)