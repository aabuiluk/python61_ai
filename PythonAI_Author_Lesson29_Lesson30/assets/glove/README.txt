GloVe 6B, 100 вимірів (Pennington, Socher, Manning 2014; Wikipedia 2014 + Gigaword 5),
ліцензія Public Domain Dedication and License (PDDL).
Оригінал — 400 000 слів, 128 МБ: gensim.downloader.load('glove-wiki-gigaword-100').
Тут 24995 слів: словник пар 27–28 + усі слова SupportFlow + синоніми служби підтримки.
Вектори ті самі, обрізано лише словник. Формат word2vec binary:
    supportflow.load_glove()  або  KeyedVectors.load_word2vec_format(path, binary=True)
