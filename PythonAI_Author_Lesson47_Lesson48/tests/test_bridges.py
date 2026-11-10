"""Explicit transport doubles: call_id matching, argument checks and saved pause."""
import json
from types import SimpleNamespace as NS
import pytest
import bridge_runtime as bridge

class API:
    def __init__(self):self.calls=[];self.responses=NS(create=self.create)
    def create(self,**kw):
        self.calls.append(kw)
        usage=NS(input_tokens=20,output_tokens=10)
        if isinstance(kw['tool_choice'],dict):
            return NS(status='completed',id='resp_tool',usage=usage,output=[NS(type='function_call',name='get_store_policy',arguments='{"topic":"refund"}',call_id='call_45')])
        assert any(isinstance(x,dict) and x.get('type')=='function_call_output' and x['call_id']=='call_45' for x in kw['input'])
        return NS(status='completed',id='resp_final',usage=usage,output_text='14 календарних днів')

def test_bridge_live_contract_and_pause(tmp_path,monkeypatch):
    monkeypatch.setattr(bridge,'PACKAGE',tmp_path)
    monkeypatch.setattr(bridge,'read_documents',lambda:[{'file':'06_returns.pdf','page':1,'source_id':'06_returns.pdf:1:0','text':'14 календарних днів'}])
    api=API();answer=bridge.bridge45('Повернення?',api=api)
    assert len(api.calls)==2 and answer['tool_calls'][0]['call_id']=='call_45'
    assert answer['sources']==['06_returns.pdf:1:0']
    paused=bridge.bridge46('Повернення?',action='draft_email',api=api)
    state=json.loads((tmp_path/'artifacts'/('bridge_approval_'+paused['approval_id']+'.json')).read_text(encoding='utf-8'))
    assert state['sent'] is False and state['status']=='pending_approval'
    before=len(api.calls)
    assert bridge.bridge46('Повернення?',action='send_email',api=api)['status']=='refused'
    assert len(api.calls)==before

def test_bridge_rejects_untrusted_tools():
    for name,args in [('delete_order',{'topic':'refund'}),('get_store_policy',{'topic':'refund','extra':1}),('get_store_policy',{'topic':'missing'})]:
        with pytest.raises(ValueError):bridge.dispatch(name,args)
