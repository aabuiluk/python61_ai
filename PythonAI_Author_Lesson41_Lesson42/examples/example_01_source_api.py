"""Розібраний навчальний приклад; API викликається тільки при запуску."""
from PythonAI_Author_Lesson41_Lesson42.api_client import send

def run():
    response = send({'instructions': 'Відповідай тільки за документом. Назви джерело.',
                     'input': 'Документ [demo]: Бібліотека відкрита з 09:00 до 18:00. Питання: коли зачиняється бібліотека?'})
    print(response.output_text)
    print('status:', response.status, 'usage:', response.usage)
    return response

if __name__ == "__main__":
    run()
