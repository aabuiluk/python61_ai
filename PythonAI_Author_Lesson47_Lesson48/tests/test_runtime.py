"""Offline transport doubles + real Qdrant; never paid calls in tests."""
import json
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
from qdrant_client import QdrantClient
from runtime import StoreRAG, validate_answer, read_documents

class API:
    def __init__(self):
        self.calls = []
        self.embeddings = NS(create=self.embed)
        self.responses = NS(create=self.respond)
    def embed(self, **kw):
        self.calls.append(('embedding', kw))
        return NS(data=[NS(index=i, embedding=[1., 0., 0.]) for i, _ in enumerate(kw['input'])], usage=NS(total_tokens=12))
    def respond(self, **kw):
        self.calls.append(('response', kw))
        return NS(id='resp_test', status='completed', output_text=json.dumps({'status':'answered','answer':'14 днів','sources':['returns.pdf:1:0']}), usage=NS(input_tokens=30, output_tokens=10))

def test_real_qdrant_upsert_persistence_and_payload(tmp_path):
    api=API(); db=QdrantClient(path=str(tmp_path/'db'))
    rag=StoreRAG(db,api,artifacts=tmp_path/'out')
    docs=[{'source_id':'returns.pdf:1:0','file':'returns.pdf','page':1,'text':'Повернення: 14 днів.'}]
    assert rag.index(docs)['points']==1
    assert rag.index(docs)['points']==1
    assert rag.search('Повернення?')[0]['page']==1
    db.close(); db=QdrantClient(path=str(tmp_path/'db'))
    assert StoreRAG(db,api,artifacts=tmp_path/'out').stats()['points']==1
    db.close()

def test_miss_never_generates_and_trace_excludes_content(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    result=rag.ask('PRIVATE_QUESTION')
    assert result['status']=='refused'
    assert not api.calls
    text=(tmp_path/'trace.jsonl').read_text(encoding='utf-8')
    assert 'PRIVATE_QUESTION' not in text and 'run_id' in text
    db.close()

def test_citation_validation_is_fail_closed():
    assert validate_answer({'status':'answered','answer':'14','sources':['missing']},['known'])['status']=='invalid'
    assert validate_answer({'status':'answered','answer':'14','sources':[]},['known'])['status']=='invalid'
    assert validate_answer({'status':'refused','answer':'Не знаю','sources':[]},['known'])['status']=='refused'

def test_model_mismatch_refuses_before_paid_query(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    rag.index([{'source_id':'a:1:0','file':'a','page':1,'text':'Test'}])
    before=len(api.calls)
    other=StoreRAG(db,api,artifacts=tmp_path,embedding_model='different')
    with pytest.raises(ValueError,match='model'):other.search('q')
    assert len(api.calls)==before
    db.close()

def test_generation_has_grounded_contract_and_usage(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    rag.index([{'source_id':'returns.pdf:1:0','file':'returns.pdf','page':1,'text':'14 днів'}])
    result=rag.ask('Коли повернути?')
    assert result['status']=='answered' and result['sources']==['returns.pdf:1:0']
    rows=[json.loads(x) for x in (tmp_path/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    assert any(x.get('input_tokens')==30 for x in rows)
    assert next(k for kind,k in api.calls if kind=='response')['store'] is False
    db.close()

def test_filter_miss_skips_responses_with_real_qdrant(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    rag.index([{'source_id':'returns.pdf:1:0','file':'returns.pdf','page':1,'text':'14 днів'}])
    result=rag.ask('Повернення?',source='does_not_exist.pdf')
    assert result['status']=='refused' and not result['hits']
    assert not any(kind=='response' for kind,_ in api.calls)
    db.close()

def test_human_pause_and_eval_metadata(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    rag.index([{'source_id':'returns.pdf:1:0','file':'returns.pdf','page':1,'text':'14 днів'}])
    result=rag.ask('Підготуй пояснення',external_action=True)
    state=json.loads((tmp_path/('approval_'+result['approval_id']+'.json')).read_text(encoding='utf-8'))
    assert state['status']=='pending_approval' and state['sent'] is False
    report=rag.evaluate([{'id':'r','question':'q','expected_files':['returns.pdf'],'expected_status':'answered'}])
    assert report['status_accuracy']==1 and report['retrieval_hit_at_k']==1
    assert 'answer' not in report['cases'][0]
    db.close()

def test_incomplete_and_api_errors_are_traced_without_message(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    hits=[{'source_id':'r','text':'14 днів'}]
    api.responses.create=lambda **kw:NS(status='incomplete',output_text='')
    with pytest.raises(ValueError,match='incomplete'):rag.generate('q',hits,'run1')
    def failure(**kw):raise RuntimeError('PRIVATE_ERROR_KEY')
    api.responses.create=failure
    with pytest.raises(RuntimeError):rag.generate('q',hits,'run2')
    trace=(tmp_path/'trace.jsonl').read_text(encoding='utf-8')
    assert 'PRIVATE_ERROR_KEY' not in trace and 'RuntimeError' in trace
    db.close()

def test_corpus_change_preserves_existing_index(tmp_path):
    api=API();db=QdrantClient(':memory:');rag=StoreRAG(db,api,artifacts=tmp_path)
    doc={'source_id':'r','file':'r','page':1,'text':'14 днів'}
    rag.index([doc]);before=len(api.calls)
    with pytest.raises(ValueError,match='Corpus changed'):rag.index([{**doc,'text':'30 днів'}])
    assert len(api.calls)==before and rag.stats()['points']==1
    db.close()
