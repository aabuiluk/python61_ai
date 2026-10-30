"""Розібраний навчальний приклад; API викликається тільки при запуску."""
import sys
from pathlib import Path
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))
from api_client import send

def run():
    import json
    tools = [{'type': 'function', 'name': 'library_hours', 'description': 'Години роботи бібліотеки',
              'parameters': {'type': 'object', 'properties': {}, 'required': [], 'additionalProperties': False}, 'strict': True}]
    history = [{'role': 'user', 'content': 'Дізнайся години роботи бібліотеки через library_hours.'}]
    first = send({'input': history, 'tools': tools, 'tool_choice': {'type': 'function', 'name': 'library_hours'}})
    if first.status != 'completed':
        raise ValueError('Незавершена відповідь')
    history.extend(first.output)
    calls = [item for item in first.output if item.type == 'function_call']
    if not calls:
        raise ValueError('API не повернув function_call')
    for call in calls:
        if call.name != 'library_hours' or json.loads(call.arguments) != {}:
            raise ValueError('Неприпустимий виклик')
        history.append({'type': 'function_call_output', 'call_id': call.call_id,
                        'output': json.dumps({'hours': '09:00–18:00'}, ensure_ascii=False)})
    second = send({'input': history, 'tools': tools, 'tool_choice': 'none'})
    print(second.output_text)
    print('status:', second.status, 'usage:', second.usage)
    return second

if __name__ == "__main__":
    run()
