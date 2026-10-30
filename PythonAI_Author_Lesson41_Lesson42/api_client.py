"""Transport for student experiments; contains no classifier/RAG/agent solution."""
import argparse
import json
import os
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent


def configuration(load_file=True):
    if load_file:
        from dotenv import load_dotenv
        load_dotenv(BASE / '.env')
    key = os.getenv('OPENAI_API_KEY', '').strip()
    if not key or key == 'replace-with-your-own-api-key':
        raise ValueError('Заповніть OPENAI_API_KEY у .env поруч із api_client.py.')
    return key, os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')


def send(payload, *, client=None, model=None):
    """Send one Responses request; SDK retries disabled to keep calls explicit."""
    if not isinstance(payload, dict) or not payload.get('input'):
        raise ValueError('JSON має містити непорожнє поле input.')
    allowed = {'input', 'instructions', 'tools', 'previous_response_id', 'max_output_tokens', 'tool_choice'}
    unknown = set(payload) - allowed
    if unknown:
        raise ValueError('Невідомі параметри: ' + ', '.join(sorted(unknown)))
    if client is None:
        from openai import OpenAI
        key, configured_model = configuration()
        model = model or configured_model
        client = OpenAI(api_key=key, timeout=30, max_retries=0)
    limit = payload.get('max_output_tokens', 600)
    if type(limit) is not int or not 1 <= limit <= 2000:
        raise ValueError('max_output_tokens: ціле число від 1 до 2000.')
    return client.responses.create(model=model, store=False, **{**payload, 'max_output_tokens': limit})


def main():
    parser = argparse.ArgumentParser(description='Один реальний OpenAI API запит із JSON-файлу.')
    parser.add_argument('request', type=Path)
    parser.add_argument('--save', type=Path, help='Записати відповідь та usage; не публікуйте приватні дані.')
    args = parser.parse_args()
    try:
        payload = json.loads(args.request.read_text(encoding='utf-8'))
        response = send(payload)
        print(response.output_text or '[Тексту немає: перегляньте output у JSON, можливо це function_call.]')
        print('status:', response.status)
        print('model:', response.model)
        print('usage:', response.usage)
        if args.save:
            args.save.parent.mkdir(parents=True, exist_ok=True)
            args.save.write_text(response.model_dump_json(indent=2), encoding='utf-8')
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        # Do not print SDK error bodies: they may echo private request data.
        print(f'API: {type(exc).__name__}, HTTP {getattr(exc, "status_code", "—")}. '
              '401: ключ; 429: квота/ліміт; 404: модель; з’єднання: мережа.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
