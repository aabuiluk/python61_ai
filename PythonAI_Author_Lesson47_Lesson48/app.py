"""Run with python -m streamlit run <package>/app.py from the repository root."""
from pathlib import Path
import sys
import json
sys.path.insert(0,str(Path(__file__).resolve().parent))
import streamlit as st
from runtime import PACKAGE, open_store, read_documents

st.set_page_config(page_title='СвітлоМаркет · Qdrant RAG',layout='wide')
st.title('СвітлоМаркет · PDF → Qdrant → OpenAI')
st.caption('Навчальний магазин. Embeddings і генерація — справжні платні OpenAI API; PDF та база — локально.')
st.info('Індексація додає фрагменти у векторну базу; ваги LLM не навчаються.')

@st.cache_resource
def resource():
    return open_store()

rag=resource()
with st.sidebar:
    st.header('Керування')
    st.caption('Спочатку перевірте PDF, потім індексуйте, потім ставте питання.')
    if st.button('1. Перевірити 10 PDF'):
        docs=read_documents()
        st.json({'files':len({d['file'] for d in docs}),'chunks':len(docs),'first':docs[0]})
    if st.button('2. Індексувати · платний API'):
        try:
            with st.spinner('OpenAI embeddings → Qdrant'):
                st.json(rag.index(read_documents()))
        except Exception as exc:
            st.error(f'{type(exc).__name__}: перевірте .env, доступ API та назву колекції. Докладніше — README.')
    if st.button('3. Статистика Qdrant'):
        st.json(rag.stats())
    top_k=st.slider('top-k',1,10,4)
    source=st.selectbox('Фільтр PDF',['Усі']+[p.name for p in sorted((PACKAGE/'data/pdf').glob('*.pdf'))])
    st.caption('Qdrant Local: dashboard відсутній. Docker Server: http://localhost:6333/dashboard')

question=st.text_input('Запитання покупця','Скільки коштує доставка Україною?')
draft=st.checkbox('Підготувати чернетку для менеджера (HITL, без надсилання)')
if st.button('4. Запитати · платний API',type='primary'):
    try:
        with st.spinner('Пошук і генерація'):
            st.session_state['result']=rag.ask(question,top_k=top_k,source=None if source=='Усі' else source,external_action=draft)
            st.session_state['result_question']=question
    except Exception as exc:
        st.error(f'{type(exc).__name__}: запит не виконано. Перевірте конфігурацію та trace.')

if 'result' in st.session_state:
    result=st.session_state['result']
    st.subheader('Відповідь і перевірений статус')
    st.write(result['answer']);st.json({k:v for k,v in result.items() if k not in {'hits','answer'}})
    with st.expander('Знайдені фрагменти, score, файл і сторінка',expanded=True):
        for hit in result['hits']:
            st.markdown(f"**{hit['source_id']}** · score={hit['score']:.4f}")
            st.write(hit['text'])
            st.download_button('Завантажити PDF '+hit['file'],(PACKAGE/'data/pdf'/hit['file']).read_bytes(),file_name=hit['file'],key=hit['source_id'])
    if st.button('Оцінити relevance / supported · ще один платний API'):
        try:
            st.json(rag.judge(st.session_state['result_question'],result['hits'],result['answer']))
        except Exception as exc:
            st.error(type(exc).__name__)

with st.expander('Trace: токени, затримка, run_id — без ключів і повних питань'):
    f=PACKAGE/'artifacts/trace.jsonl'
    rows=[json.loads(line) for line in f.read_text(encoding='utf-8').splitlines()] if f.exists() else []
    st.dataframe(rows[-60:],width='stretch')
st.caption('Перед CLI в Qdrant Local зупиніть Streamlit: один процес володіє локальним сховищем. Для паралельної роботи — Docker Server.')
