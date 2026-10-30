# file: tool_validation.py
import json
from decimal import Decimal

def execute_tool(name: str, raw_arguments: str):
    if name != 'course_total':
        raise ValueError('Інструмент не дозволено')
    args = json.loads(raw_arguments)
    if set(args) != {'lessons', 'price_per_lesson'}:
        raise ValueError('Невірні поля')
    if type(args['lessons']) is not int:
        raise TypeError('lessons має бути цілим')
    if type(args['price_per_lesson']) not in (int, float):
        raise TypeError('price_per_lesson має бути числом')
    lessons, price = args['lessons'], args['price_per_lesson']
    if not (1 <= lessons <= 100 and 0 <= price <= 10000):
        raise ValueError('Значення поза межами')
    return {'total': float(Decimal(str(lessons)) * Decimal(str(price)))}

print(execute_tool('course_total', '{"lessons":8,"price_per_lesson":25}'))
