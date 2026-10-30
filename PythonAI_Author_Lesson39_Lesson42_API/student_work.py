"""Ваші реалізації; імпорт цього файлу не надсилає API-запитів."""
from api_client import send


def classify(texts, ask=send):
    """Завдання 02: перевірені мітки для відгуків."""
    raise NotImplementedError("Реалізуйте за карткою завдання")


def chunks(documents, size=40, overlap=10):
    """Завдання 05: фрагменти з походженням."""
    raise NotImplementedError("Реалізуйте за карткою завдання")


def retrieve(question, documents, k=2):
    """Завдання 06: top-k із додатною схожістю."""
    raise NotImplementedError("Реалізуйте за карткою завдання")


def rag(question, documents, ask=send):
    """Завдання 07: відповідь і перевірені джерела."""
    raise NotImplementedError("Реалізуйте за карткою завдання")


def execute(name, arguments):
    """Завдання 09: allowlist і перевірка параметрів."""
    raise NotImplementedError("Реалізуйте за карткою завдання")


def agent(question, ask=send, max_steps=3):
    """Завдання 10: обмежений цикл інструментів."""
    raise NotImplementedError("Реалізуйте за карткою завдання")
