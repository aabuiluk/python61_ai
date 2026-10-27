"""**Факт. Vertex AI організовує доступ до моделей і ML-процесів усередині Google Cloud-проєкту.**

Схема запиту: застосунок → автентифікація службового облікового запису → IAM-дозвіл →
проєкт і доступний регіон → API моделі або керований endpoint → відповідь → журнал і метрики.
Cloud project групує ресурси, квоти та зв'язок із billing account. IAM визначає, хто може
викликати ресурс; квота обмежує використання; білінг обліковує витрати. Це різні механізми:
дозвіл IAM не скасовує квоту, а budget alert зазвичай повідомляє про поріг і не є гарантією
автоматичної зупинки витрат.

Платформа охоплює доступ до генеративних моделей, роботу з моделями в Model Garden,
навчання, розгортання, пайплайни й моніторинг; конкретні функції та моделі мають власні
вимоги й доступність. Для виклику керованої генеративної моделі не завжди створюють
власний endpoint: не змішуйте цей сценарій із розгортанням своєї навченої моделі.

**Безкоштовний маршрут тут — читання документації та локальна схема, не запуск Cloud.**
Відкрийте [огляд Vertex AI](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform),
знайдіть розділи про generative AI та ML workflow. У [IAM-огляді](https://cloud.google.com/vertex-ai/docs/general/access-control)
знайдіть ролі доступу; в [огляді квот](https://cloud.google.com/vertex-ai/docs/quotas) — види лімітів.
Не створюйте проєкт, billing account чи trial. Код нижче перевіряє навчальну конфігурацію,
а не реальні дозволи Google Cloud і не готовність до продакшену.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
architecture = {"client":"shop_app","identity":"service_account","permission":"model_invoke",
                "project":"training_diagram_only","region":"check_model_availability",
                "model_access":"managed_api","observability":["logs","usage"],"mode":"documentation_only"}
print(json.dumps(architecture,ensure_ascii=False,indent=2))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Identity + IAM', 'Project / region', 'Model API', 'Logs + billing']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 14: data flow (not model measurements)')
fig.tight_layout()
plt.show()
