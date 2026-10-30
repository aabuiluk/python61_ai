# file: review_pipeline.py
from classifier_live import client, MODEL

def call(instructions, text):
    r = client.responses.create(model=MODEL, instructions=instructions,
                                input=text, max_output_tokens=300)
    return r.output_text

complaint = 'Урок скасували за 10 хвилин до початку. Я обурений.'
draft = call('Напиши коротку ввічливу відповідь служби підтримки.', complaint)
critique = call('Перевір текст на емпатію, конкретність і необґрунтовані обіцянки. '
                'Назви 3 конкретні правки.', draft)
final = call('Відредагуй відповідь за зауваженнями. Не обіцяй компенсації без підтвердження.',
             f'Чернетка:\n{draft}\nЗауваження:\n{critique}')
print('ЧЕРНЕТКА:', draft)
print('ПЕРЕВІРКА:', critique)
print('ФІНАЛ:', final)
