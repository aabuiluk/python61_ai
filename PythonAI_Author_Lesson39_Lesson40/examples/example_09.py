"""**Факт. Інтерфейс чату, програмний API і хмарна платформа — різні способи роботи.**

Google AI Studio зручний для ручної перевірки промптів. Gemini Developer API дає програмний
доступ; для нього окремо керують ключами й квотами. Vertex AI — платформа Google Cloud
із проєктами, IAM та керованими сервісами. У цій парі Vertex вивчаємо за документацією,
не активуємо billing, пробні кредити чи endpoint. Безкоштовний кредит — не безкоштовний сервіс.

Відкрийте [огляд Vertex AI](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)
та [огляд Gemini API](https://ai.google.dev/gemini-api/docs). Порівняйте призначення й спосіб доступу.
Модель обирайте за потрібним входом/виходом, доступністю й фактичними умовами сьогодні;
назви моделей та квоти змінюються. Не вчіть фіксовану назву як вічний стандарт.

Локальний FakeClient нижче імітує тільки інтерфейс. Він повертає ручну відповідь і
кількість слів, не токенів. Його лог не є звітом реального провайдера.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
class FakeClient:
    def generate(self, prompt):
        return {"text":'{"book_id":"b01","price":320}', "input_words":len(prompt.split()), "mode":"fixture"}
response = FakeClient().generate("Яка ціна b01?")
print(response)

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Browser', 'API interface', 'Cloud platform', 'Choose access']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 9: data flow (not model measurements)')
fig.tight_layout()
plt.show()
