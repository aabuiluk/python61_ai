# file: chunks_demo.py
from dataclasses import dataclass

@dataclass
class Chunk:
    id: str
    title: str
    text: str

source = {'id': 'DOC-1', 'title': 'Правила магазину',
          'text': 'Магазин працює з 09:00 до 19:00.\n\nСамовивіз доступний у робочі години.\n\nПовернення товару здійснюється за правилами магазину.'}
paragraphs = [p.strip() for p in source['text'].split('\n\n') if p.strip()]
chunks = [Chunk(f"{source['id']}-{i+1}", source['title'], p)
          for i, p in enumerate(paragraphs)]
for chunk in chunks:
    print(chunk.id, chunk.title, chunk.text)
