# file: api_check.py
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY', '')
if not key:
    raise RuntimeError('OPENAI_API_KEY не задано у середовищі')
print('Ключ присутній у середовищі (сам ключ не виводимо)')
# Відкликати скомпрометований ключ у кабінеті провайдера.
