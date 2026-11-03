"""43.1 · Model → chain → retrieval → agent

**Факт 3. Фреймворк стандартизує компонування коду навколо моделі, а не замінює модель.**

Model-вузол отримує повідомлення й повертає результат. Chain задає відому послідовність:
підготувати дані → сформувати prompt → модель → parser. Retrieval знаходить документи.
Agent у циклі обирає наступну дію за станом і observation. Це ролі компонентів, а не
обов’язкова сходинка складності: RAG-chain може ніколи не бути агентом.

Сирого SDK досить для одного виклику з простим контролем. Коли з’являються повторювані
шаблони, парсери та кілька конекторів, стандартні інтерфейси економлять код. Натомість
додаються залежності, зміни API та вимога розуміти типи даних між вузлами.
Не переписуйте робочий retrieval заради модної назви: обгорніть перевірену функцію.

У прикладі карта зв’язує власні функції з компонентами майбутнього DocFlow. На 44 ми
використаємо справжні Runnable. На 43 порівнюємо архітектури; список назв не є запуском пакетів.
"""
import json

# %% Основний код
layers = {"model":"fixture_model або окремий провайдерський конектор",
          "chain":"context → prompt → model → parser",
          "retrieval":"retrieve(question,k)","agent":"цикл tool/observation зі станом"}
print(json.dumps(layers,ensure_ascii=False,indent=2))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Model', 'Chain', 'Retrieval', 'Agent']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 3: data flow, not model measurements')
fig.tight_layout()
plt.show()
