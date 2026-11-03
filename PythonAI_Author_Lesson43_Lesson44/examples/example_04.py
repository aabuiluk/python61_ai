"""43.2 · LangChain, LlamaIndex та Vertex AI

**Факт 4. Бібліотека оркестрації та керована Cloud-платформа можуть працювати разом.**

LangChain надає компоненти й інтеграції для LLM-застосунків; у нашій 44 використовуємо
langchain-core для prompt, Runnable та parser. LlamaIndex часто розглядають першою
кандидатурою, коли головна складність — завантаження, індексація та retrieval документів.
Обидва екосистемні підходи мають перекриття: це не правило «лише агенти» проти «лише RAG».

Vertex AI у програмі — керована Google Cloud-платформа доступу до моделей та ML-сервісів.
Вона вирішує інший шар: проєкт, ідентичність, IAM, регіон, квоти, облік витрат.
Можна мати LangChain-застосунок, що використовує провайдерський сервіс у Cloud. А можна
написати звичайний SDK-клієнт без LangChain. Питання «що краще» замініть на «яку вимогу покриває».

Для трьох правил магазину спочатку лишаємо існуючий TF-IDF. Для великого неоднорідного
корпусу оцінюємо конектори, метадані, chunking, оновлення та якість retrieval.
Не встановлюйте LlamaIndex із типовими модельними провайдерами заради таблиці: це може
створити непотрібні вимоги до ключів. Огляд безкоштовний, а запуски моделей — окрема умова провайдера.
"""
import json

# %% Основний код
choices = [
 {"need":"компонування prompt/model/parser","candidate":"LangChain","layer":"application"},
 {"need":"завантаження й індексація багатьох документів","candidate":"LlamaIndex","layer":"data"},
 {"need":"керований Cloud-доступ та IAM","candidate":"Vertex AI","layer":"platform"}]
print(json.dumps(choices,ensure_ascii=False,indent=2))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Requirements', 'Data pipeline', 'Library', 'Platform']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 4: data flow, not model measurements')
fig.tight_layout()
plt.show()
