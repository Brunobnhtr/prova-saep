"""Checagens da cobertura e integridade; não valida respostas ou pertinência técnica."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/acervo-ampliado'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
qs=load(OUT/'catalogo-global.json')['questions'];s=load(OUT/'resumo-global.json');ids={q['source_id'] for q in qs}
tests=[]
def check(name,result):
 tests.append({'check':name,'passed':bool(result)})
check('all 9791 IDs unique and reconciled',len(qs)==len(ids)==s['INDEX_TOTAL']==9791)
check('classified plus unclassified equals total',s['CLASSIFIED']+s['UNCLASSIFIED']==len(ids))
check('all answers remain unresolved',all(q['answer_status']=='UNRESOLVED' for q in qs))
check('source lots unchanged since scan',all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256'] for f in s['SOURCE_FILES']))
queues=[load(p) for p in sorted((OUT/'por-modulo').glob('*.json'))];mids={q['module'] for q in queues}
check('35 module queues',len(queues)==35)
check('no invented module IDs',all(set(c['module'] for c in q['module_candidates'])<=mids for q in qs))
check('module totals reconcile',sum(q['total_candidates'] for q in queues)==s['MODULE_ASSIGNMENTS'])
check('queue references exist',all(d['source_id'] in ids for q in queues for d in q['candidate_details']))
check('relevance partitions each queue',all(q['high_relevance']+q['medium_relevance']+q['low_relevance']==q['total_candidates'] for q in queues))
check('all prior topic joins audited',sum(bool(q['prior_topics']) for q in qs)==s['PRIOR_TOPIC_JOINS'])
check('VF detected from actual two-option labels',sum('TRUE_FALSE' in q['probable_types'] for q in qs)==1031)
check('missing visuals flagged for inspection rather than invalidated',all(q['editorial_decision']=='INSPECT' for q in qs if q['image_status']=='IMAGE_MISSING'))
check('numeric variant candidates reference valid IDs',all(set(g)<=ids for g in load(OUT/'redundancias-candidatas.json')['numeric_text_variants']))
check('family groups plus unassigned cover exactly the catalog',set(load(OUT/'familias-semanticas.json')['unassigned'])|{i for group in load(OUT/'familias-semanticas.json')['families'].values() for i in group}==ids)
report={'passed':sum(t['passed'] for t in tests),'failed':sum(not t['passed'] for t in tests),'checks':tests,'scope':'Coverage and structural integrity only; does not certify semantic classifications.'}
(OUT/'validacao-global.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2));assert report['failed']==0
