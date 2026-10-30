"""Local Streamlit UI -> real OpenAI API -> local tools/RAG."""
import streamlit as st
from agent import run_agent
from vectors import rag

st.title('Помічник українського магазину')
mode=st.radio('Режим',['RAG','Агент'])
question=st.text_input('Питання')
if st.button('Запитати') and question.strip():
    with st.spinner('Реальний запит OpenAI API...'):
        try:
            if mode=='RAG': st.json(rag(question))
            else: st.write(run_agent(question))
        except Exception as exc:
            st.error(type(exc).__name__+': перевірте індекс, .env, доступ до моделі та контракт відповіді.')
st.caption('Дані, індекс та оркестрація локальні. Embeddings і генерація виконуються OpenAI API та можуть коштувати грошей.')
