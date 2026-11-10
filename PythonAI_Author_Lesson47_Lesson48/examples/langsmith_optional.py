"""Explicit opt-in: send only sanitized local run metadata to LangSmith."""
from pathlib import Path
import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE
from dotenv import load_dotenv

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--send',action='store_true');a=p.parse_args()
    load_dotenv(PACKAGE/'.env')
    trace=PACKAGE/'artifacts/trace.jsonl'
    rows=[json.loads(x) for x in trace.read_text(encoding='utf-8').splitlines()]
    last=rows[-1]['run_id']
    clean=[{k:r.get(k) for k in ('run_id','stage','status','duration_ms')} for r in rows if r['run_id']==last]
    print(json.dumps(clean,ensure_ascii=False,indent=2))
    if not a.send:
        print('Preview only. Add --send to upload these metadata.');return
    if not os.getenv('LANGSMITH_API_KEY'):raise ValueError('Set LANGSMITH_API_KEY in local .env')
    from langsmith import Client
    client=Client();run_id=uuid.uuid4()
    client.create_run(name='store-local-summary',inputs={'local_run_id':last},run_type='chain',id=run_id,
                      project_name=os.getenv('LANGSMITH_PROJECT','store-47-48'))
    client.update_run(run_id,outputs={'events':clean},end_time=datetime.now(timezone.utc))
    print('Uploaded sanitized metadata. Open LangSmith project store-47-48 → Runs.')

if __name__=='__main__':main()
