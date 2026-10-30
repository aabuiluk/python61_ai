# file: retrieval_metrics.py
expected = {'Коли працює магазин?': 'DOC-1', 'Як оплатити замовлення?': 'DOC-2'}
retrieved = {'Коли працює магазин?': ['DOC-1', 'DOC-3'],
             'Як оплатити замовлення?': ['DOC-4', 'DOC-2']}
hit_at_2 = sum(expected[q] in retrieved[q][:2] for q in expected) / len(expected)
print('Hit@2:', hit_at_2)
assert hit_at_2 == 1.0
