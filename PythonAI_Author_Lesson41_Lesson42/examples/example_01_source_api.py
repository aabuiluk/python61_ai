"""Розібраний навчальний приклад; API викликається тільки при запуску."""
import sys
from pathlib import Path
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))
from api_client import send

def run():
    response = send({'instructions': 'Відповідай тільки за документом. Назви джерело.',
                     'input': 'Документ [demo]: Бібліотека відкрита з 09:00 до 18:00. Питання: коли зачиняється бібліотека?'})
    print(response.output_text)
    print('status:', response.status, 'usage:', response.usage)
    return response

if __name__ == "__main__":
    run()
