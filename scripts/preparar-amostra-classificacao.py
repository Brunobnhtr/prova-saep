from pathlib import Path
import json,random,collections
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/acervo-ampliado'
qs=json.loads((OUT/'catalogo-global.json').read_text(encoding='utf-8'))['questions'];byid={q['source_id']:q for q in qs}
base=Path(r'C:\dev\extrator de perguntas\eletrica_eletronica\questoes');raw={}
for p in base.glob('lote_*.json'):
 for q in json.loads(p.read_text(encoding='utf-8-sig'))['questoes']:raw[q['codigo']]=q
rng=random.Random(20261006);sample=[];seen=set()
def add(q,stratum):
 if q['source_id'] not in seen:
  seen.add(q['source_id']);sample.append({'source_id':q['source_id'],'stratum':stratum,'v1_module':q['primary_module'],'v1_confidence':q['theme_classification_confidence'],'statement':q['statement'],'alternatives':raw[q['source_id']]['alternativas'],'image_references':q['image_references'],'metadata':q['current_subthemes']})
for sid in ['Q4148970','Q4148977','Q4150424','Q4151541']:add(byid[sid],'MANDATORY_REGRESSION')
modules=json.loads((OUT/'cruzamento-35-temas.json').read_text(encoding='utf-8-sig'))['modulos']
for m in modules:
 for confidence,count in [('HIGH',2),('MEDIUM',1),('LOW',1)]:
  candidates=[q for q in qs if q['primary_module']==m['modulo'] and q['theme_classification_confidence']==confidence and not q['has_image'] and 20<len(q['statement'] or '')<=450 and sum(len(a['texto']) for a in raw[q['source_id']]['alternativas'])<=600]
  rng.shuffle(candidates)
  for q in candidates[:count]:add(q,m['modulo']+':'+confidence)
unclassified=[q for q in qs if not q['primary_module'] and not q['has_image'] and 20<len(q['statement'] or '')<=450 and sum(len(a['texto']) for a in raw[q['source_id']]['alternativas'])<=600];rng.shuffle(unclassified)
for q in unclassified:
 if len(sample)>=150:break
 add(q,'UNCLASSIFIED')
assert len(sample)==150,len(sample)
(OUT/'amostra-classificacao-revisao.json').write_text(json.dumps({'seed':20261006,'selection_bias':'Amostra dirigida por estrato V1, enunciados curtos e majoritariamente sem imagem. Não representativa estatisticamente; expectativas serão anotadas pelo agente, não pelo classificador.','questions':sample},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('150 selected; module strata:',len({q['v1_module'] for q in sample if q['v1_module']}))
