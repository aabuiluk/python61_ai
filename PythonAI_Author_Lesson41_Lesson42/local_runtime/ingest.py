"""Local TXT/PDF/CSV loader with source provenance; no API calls."""
import csv
from pathlib import Path

def load_sources(paths):
    documents=[]
    for raw in paths:
        path=Path(raw)
        if path.suffix.lower()=='.txt':
            documents.append({'id':path.stem,'source':path.name,'text':path.read_text(encoding='utf-8')})
        elif path.suffix.lower()=='.csv':
            with path.open(encoding='utf-8',newline='') as stream:
                for row_number,row in enumerate(csv.DictReader(stream),2):
                    price=int(row['price_uah'])
                    if price<0: raise ValueError('Від’ємна ціна')
                    documents.append({'id':'product-'+row['id'],'source':path.name,'row':row_number,
                                      'text':f"{row['name']} коштує {price} грн. Місто: {row['city']}."})
        elif path.suffix.lower()=='.pdf':
            from pypdf import PdfReader
            for page_number,page in enumerate(PdfReader(path).pages,1):
                text=(page.extract_text() or '').strip()
                if not text: raise ValueError('PDF без текстового шару: потрібне OCR')
                documents.append({'id':f'{path.stem}-p{page_number}','source':path.name,'page':page_number,'text':text})
        else: raise ValueError('Непідтримуваний формат')
    if len({d['id'] for d in documents})!=len(documents): raise ValueError('Повторні ID')
    return documents

def chunk_documents(documents,size=80,overlap=15):
    if not 0<=overlap<size: raise ValueError('Неправильні size/overlap')
    result=[]
    for doc in documents:
        words=doc['text'].split()
        for start in range(0,len(words),size-overlap):
            result.append({**doc,'id':doc['id']+':'+str(start),'document_id':doc['id'],'start':start,
                           'text':' '.join(words[start:start+size])})
            if start+size>=len(words): break
    return result

if __name__=='__main__':
    data=Path(__file__).resolve().parents[1]/'data'
    docs=load_sources([data/'local_hours.txt',data/'local_products.csv',data/'local_delivery.pdf'])
    for doc in chunk_documents(docs): print(doc)
