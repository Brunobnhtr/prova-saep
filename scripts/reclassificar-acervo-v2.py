from pathlib import Path
import json,hashlib,copy,collections,importlib.util
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/acervo-ampliado'
spec=importlib.util.spec_from_file_location('concepts',ROOT/'scripts/classificador-conceitos-v2.py');classifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(classifier)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run():
 original=OUT/'catalogo-global.json';before=hashlib.sha256(original.read_bytes()).hexdigest();v1=load(original)['questions'];byid={r['source_id']:r for r in v1}
 options={}
 for p in Path(r'C:\dev\extrator de perguntas\eletrica_eletronica\questoes').glob('lote_*.json'):
  for q in load(p)['questoes']:options[q['codigo']]=q['alternativas']
 images={'Q4148970':'Reversão de motor trifásico: K1 e K2 invertem duas fases; selo e intertravamento mecânico e elétrico.','Q4148977':'Ponte de Wheatstone com voltímetro entre pontos médios, quatro braços resistivos e extensômetro; equilíbrio da ponte.','Q4150424':'Identificação de transistor; símbolos de FET Q1 e Q2 em circuito apresentado.','Q4027618':'Circuito eletropneumático com válvula 5/2, cilindro, botões S1/S2, relé K1 e solenoide 1Y1; sequência de acionamento.'}
 save(OUT/'observacoes-visuais-classificacao-v2.json',{'reviewer':'AGENT','scope':'Somente quatro imagens efetivamente abertas e inspecionadas nesta etapa; observações não contêm gabarito.','observations':images})
 rows=[]
 for r in v1:
  n=copy.deepcopy(r);n.update(classifier.classify(r,options[r['source_id']],images.get(r['source_id'],'')));n['classification_version']=2;n['classification_status']='PRELIMINARY';n['answer_status']='UNRESOLVED'
  n['v1_inspection_reasons']=r['inspection_reasons']
  n['classification_inspection_reasons']=([n['unclassified_reason']] if n['unclassified_reason'] else [])+(['THEMATIC_TIE'] if n['thematic_tie'] else [])+(['UNINSPECTED_VISUAL_CONTEXT'] if n['family_status']=='PRELIMINARY_REQUIRES_IMAGE' else [])+(['CRITICAL_NORMATIVE_CONTEXT'] if 'SAFETY_NORM' in n['probable_types'] else [])+(['HIGH_INTERACTION_REVIEW'] if n['interaction_candidate']=='HIGH' else [])
  rows.append(n)
 save(OUT/'catalogo-global-v2.json',{'method':'Taxonomia técnica hierárquica v2; precedência de conceitos específicos, assuntos originais, apoio dos tópicos anteriores e alternativas. Regras determinísticas auditáveis, não modelo semântico certificado.','v1_sha256':before,'questions':rows})
 definitions=[];parents=set()
 for concept,parent,module,specificity,pattern in classifier.DEFINITIONS:
  if concept==parent:parent='TECHNICAL_CONCEPTS'
  definitions.append({'concept':concept,'parent':parent,'curricular_module':module,'specificity':specificity,'frame_pattern':pattern});parents.add(parent)
 definitions.append({'concept':'UNSPECIFIED_RESISTOR_CIRCUIT','parent':'INSUFFICIENT_CONTEXT','curricular_module':None,'specificity':0,'frame_pattern':'Circuito resistivo referenciado, contexto insuficiente; não inferir topologia.'});parents.add('INSUFFICIENT_CONTEXT')
 defined={d['concept'] for d in definitions}
 taxonomy={'version':2,'evidence_order':['A_EXPLICIT_TECHNICAL_CONCEPT_OR_INSPECTED_IMAGE','B_ORIGINAL_SUBJECT','C_PRIOR_TOPIC_SUPPORT_ONLY','D_COMPONENT_APPLICATION_CONTEXT','E_MATHEMATICAL_VISUAL_STRUCTURE','F_GENERIC_WORDS_NON_DECISIVE'],'definitions':definitions,'parent_nodes':[{'concept':p,'parent':'TECHNICAL_CONCEPTS'} for p in sorted(parents) if p!='TECHNICAL_CONCEPTS' and p not in defined],'limits':'Deterministic technical frames are not exhaustive semantic understanding. Alternatives support compatible explicit concepts; distractors cannot establish a primary concept alone.'}
 save(OUT/'taxonomia-conceitos-v2.json',taxonomy)
 groups=collections.defaultdict(list);variants=collections.defaultdict(list)
 for r in rows:
  if r['semantic_family']:
   groups[r['semantic_family']].append(r['source_id'])
   # Family + response structure: pedagogical variants, not asserted duplicates.
   intent='CLASSIFY_PROPOSITIONS' if 'MULTIPLE_PROPOSITIONS' in r['probable_types'] else 'JUDGE_STATEMENT' if 'TRUE_FALSE' in r['probable_types'] else 'COMPUTE_QUANTITY' if 'CALCULATION' in r['probable_types'] else 'READ_DIAGRAM' if 'DIAGRAM' in r['probable_types'] else 'SELECT_CONCEPT'
   key=r['semantic_family']+'::'+intent;r['semantic_variant_group']=key;variants[key].append(r['source_id'])
  else:r['semantic_variant_group']=None
 save(OUT/'catalogo-global-v2.json',{'method':'Hierarchical technical-frame classification v2; provisional, no answers generated.','v1_sha256':before,'questions':rows})
 save(OUT/'familias-semanticas-v2.json',{'families':dict(groups),'unassigned':[r['source_id'] for r in rows if not r['semantic_family']],'taxonomy':'taxonomia-conceitos-v2.json'})
 save(OUT/'variantes-semanticas-v2.json',{'criterion':'Conceito central + estrutura de resposta; é agrupamento pedagógico candidato, não certificação de equivalência semântica.','groups':{k:v for k,v in variants.items() if len(v)>1},'deletions':0})
 unclassified=[{'source_id':r['source_id'],'v1_unclassified':byid[r['source_id']]['primary_module'] is None,'v2_primary_module':r['primary_module'],'unclassified_reason':r['unclassified_reason'],'primary_concept':r['primary_concept'],'inspection_priority':r['inspection_priority'],'evidence':r['classification_evidence']} for r in rows if byid[r['source_id']]['primary_module'] is None or r['primary_module'] is None]
 save(OUT/'unclassified-analysis.json',{'scope':'Todas as 878 questões UNCLASSIFIED V1, mais novos itens sem módulo. Razões são preliminares; reconhecer conceito sem módulo não resolve a lacuna curricular.','reason_counts':dict(collections.Counter(r['unclassified_reason'] or 'RECLASSIFIED' for r in unclassified)),'questions':unclassified})
 modules=load(OUT/'cruzamento-35-temas.json')['modulos'];queues=[]
 for m in modules:
  primary=[r for r in rows if r['primary_module']==m['modulo']];secondary=[r for r in rows if m['modulo'] in r['secondary_modules']]
  q={'module':m['modulo'],'title':m['titulo'],'primary_count':len(primary),'secondary_count':len(secondary),'confidence_counts':dict(collections.Counter(r['theme_classification_confidence'] for r in primary)),'primary_ids':[r['source_id'] for r in sorted(primary,key=lambda r:(r['inspection_priority'],r['source_id']))],'secondary_ids':[r['source_id'] for r in secondary]}
  save(OUT/'por-modulo-v2'/f"{m['modulo']}.json",q);queues.append(q)
 comparison=collections.Counter()
 for r in rows:
  old=byid[r['source_id']]
  comparison['PRIMARY_MODULE_CHANGED']+=r['primary_module']!=old['primary_module']
  comparison['LEFT_UNCLASSIFIED']+=old['primary_module'] is None and r['primary_module'] is not None
  comparison['OUT_OF_CURRICULUM']+=r['unclassified_reason']=='OUT_OF_CURRICULUM'
  comparison['NEW_SEMANTIC_FAMILY']+=old['semantic_family'] is None and r['semantic_family'] is not None
  comparison['CHANGED_SEMANTIC_FAMILY']+=old['semantic_family'] is not None and r['semantic_family']!=old['semantic_family']
  comparison['HIGH_DOWNGRADED']+=old['theme_classification_confidence']=='HIGH' and r['theme_classification_confidence']!='HIGH'
  comparison['LOW_MEDIUM_PROMOTED']+=old['theme_classification_confidence'] in ['LOW','MEDIUM'] and r['theme_classification_confidence']=='HIGH'
  comparison['THEMATIC_TIES_RESOLVED']+='THEMATIC_TIE' in old['inspection_reasons'] and not r['thematic_tie']
 total=len(rows);classified=sum(r['primary_module'] is not None for r in rows)
 summary={'TOTAL_QUESTIONS':total,'CLASSIFIED':classified,'UNCLASSIFIED':total-classified,'SEMANTIC_FAMILY_ASSIGNED':sum(bool(r['semantic_family']) for r in rows),'MODULE_ASSIGNMENTS':sum(bool(r['primary_module'])+len(r['secondary_modules']) for r in rows),'HIGH_INTERACTION_POTENTIAL':sum(r['interaction_candidate']=='HIGH' for r in rows),'CONFIDENCE_COUNTS':dict(collections.Counter(r['theme_classification_confidence'] for r in rows)),'INSPECTION_PRIORITY_COUNTS':dict(collections.Counter(r['inspection_priority'] for r in rows)),'V1_COMPARISON':dict(comparison),'V1_UNCHANGED':hashlib.sha256(original.read_bytes()).hexdigest()==before,'ANSWERS_UNRESOLVED':all(r['answer_status']=='UNRESOLVED' for r in rows),'MODULE_QUEUES':[{k:v for k,v in q.items() if k not in ['primary_ids','secondary_ids']} for q in queues]}
 save(OUT/'resumo-global-v2.json',summary);assert total==9791 and summary['V1_UNCHANGED'];print(json.dumps({k:v for k,v in summary.items() if k!='MODULE_QUEUES'},indent=2))
if __name__=='__main__':run()
