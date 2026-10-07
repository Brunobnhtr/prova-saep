"""Triagem global reproduzível, sem gabaritos e sem mutações no acervo externo.

Classificação contextual determinística: metadados + enunciado + tópicos prévios.
Não equivale à leitura semântica humana de 9.791 itens. Incertezas são explícitas.
"""
from pathlib import Path
import json, re, html, unicodedata, hashlib, collections, argparse

ROOT=Path(__file__).resolve().parents[1]
def norm(s):
    return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFD',html.unescape(s or '').lower()) if unicodedata.category(c)!='Mn')).strip()
def match(p,s):return bool(re.search(p,s))
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Concepts require contextual phrases, rather than isolated words such as bloqueio.
RULES={
'S01':r'desenergiza|reenergiza|ausencia de tensao|bloqueio.{0,55}(eletric|energia|seccion)|seccion.{0,55}(segur|nr.?10)',
'S02':r'nr.?35|trabalho em altura|equipamento de protecao individual|\bepi\b|zona controlada|trabalhador.{0,30}(autoriz|habilit|qualific)',
'F01':r'grandeza eletrica|sistema internacional|unidade.{0,25}(ampere|volt|ohm)|carga eletrica|corrente continua|corrente alternada',
'M01':r'multimetro|voltimetro|amperimetro|alicate amper|escala.{0,30}(med|instrument)',
'F02':r'lei de ohm|resist.{0,35}(equivalente|serie|paralelo)|kirchhoff|divisor de (tensao|corrente)',
'F03':r'frequencia|reatancia|impedancia|\brlc\b|senoidal|fasor|forma de onda',
'F04':r'fator de potencia|potencia (ativa|reativa|aparente)|energia eletrica|potencia.{0,30}(eletric|trifas)|\bkwh\b',
'I03':r'unifilar|multifilar|\bcad\b|simbologia.{0,25}eletric|simbolo.{0,25}eletric',
'R01':r'alimentador|poste|rede.{0,25}(distribuicao|radial|anel)|estrutura.{0,20}rede',
'H01':r'valvula|atuador pneumatico|cilindro pneumatico|hidraul|pneumat',
'A01':r'boole|tabela.{0,10}verdade|porta logica|binari|\bladder\b',
'E01':r'placa.{0,20}motor|velocidade.{0,30}(motor|sincron)|escorregamento|rotacao.{0,20}motor',
'T01':r'transformador|relacao de transformacao',
'T02':r'transformador.{0,15}(corrente|potencial)|medicao indireta|rele.{0,20}(protecao|distancia)',
'R02':r'subestacao|barramento|seccionadora|manobra.{0,25}(rede|eletric)',
'I01':r'tomada|iluminacao|previsao.{0,20}carga|luminaria',
'P01':r'dimensionamento.{0,25}(condutor|cabo)|secao.{0,25}(condutor|cabo)|ampacidade|fator de correcao|metodo de instalacao',
'P02':r'disjuntor|fusivel|curto.circuito|curva.{0,20}disparo',
'I02':r'interruptor|fotocelula|fotoeletric|rele.{0,15}foto',
'P03':r'diferencial.residual|\bidr\b|\bddr\b|dispositivo dr',
'M02':r'continuidade|resistencia de isolamento|megohmetro|megometro',
'S03':r'prontuario|extra.baixa tensao|classificacao.{0,20}tensao|documentacao.{0,20}eletric',
'V01':r'fotovoltaic|painel solar|celula solar|modulo solar|irradiancia',
'D01':r'manutencao (preventiva|preditiva|corretiva)|plano de manutencao|inspecao.{0,20}manutencao',
'D02':r'termograf|ponto quente|diagnostico.{0,25}falha|localizacao.{0,25}defeito',
'E02':r'fechamento.{0,25}motor|bobina.{0,25}motor|motor.{0,25}(trifas|monofas)|enrolamento.{0,25}motor',
'E03':r'contator|intertravamento|partida direta|reversao|contato.{0,15}selo',
'H02':r'eletropneumat|sequencia.{0,30}(cilindro|pneumatic)|solenoide.{0,30}valvula',
'A02':r'\bclp\b|controlador logico|controle sequencial|entrada.{0,20}saida',
'E06':r'inversor.{0,20}frequencia|soft.starter|parametriz',
'E04':r'estrela.triangulo|partida compensadora|autotransformador.{0,30}partida',
'A03':r'sensor.{0,20}(presenca|nivel|proximidade)|alarme|controle de nivel',
'E05':r'dahlander|duas velocidades|comutacao de polos',
'P04':r'aterramento|equipotencial|esquema.{0,10}(tn|tt|it)\b',
'P05':r'\bspda\b|\bdps\b|descarga atmosferica|para.raio',
}
FAMILIES=[
('NR10_DEENERGIZATION',r'desenergiza|reenergiza|ausencia de tensao'),
('OHMS_LAW_DIRECT_RESISTANCE',r'(resistencia.{0,80}(corrente|tensao)|(corrente|tensao).{0,80}resistencia)',r'lei de ohm|\d'),
('PARALLEL_EQUIVALENT_RESISTANCE',r'resist.{0,100}paralelo|paralelo.{0,100}resist'),
('SERIES_EQUIVALENT_RESISTANCE',r'resist.{0,100}serie|serie.{0,100}resist'),
('KIRCHHOFF_KCL',r'lei.{0,15}nos|kirchhoff.{0,30}corrente'),
('KIRCHHOFF_KVL',r'lei.{0,15}malhas|kirchhoff.{0,30}tensao'),
('THREE_PHASE_POWER',r'potencia.{0,80}trifas|trifas.{0,80}potencia'),
('POWER_DC',r'potencia.{0,80}corrente continua'),
('MULTIMETER_VOLTAGE',r'(multimetro|voltimetro).{0,100}tensao|tensao.{0,100}(multimetro|voltimetro)'),
('MULTIMETER_CURRENT',r'(multimetro|amperimetro).{0,100}corrente|corrente.{0,100}(multimetro|amperimetro)'),
('CONTACTOR_NO_NC',r'contato.{0,30}(normalmente|aberto|fechado)'),
('MOTOR_PROTECTION',r'(motor.{0,80}(protecao|sobrecarga)|(protecao|sobrecarga).{0,80}motor)'),
('LADDER_SEAL_IN',r'(ladder|contato).{0,50}selo|selo.{0,50}(ladder|contato)'),
('RLC_PHASOR',r'\brlc\b|fasor'),
('CONTINUITY_TEST',r'continuidade'),
('INSULATION_TEST',r'resistencia de isolamento|megohmetro|megometro'),
('VOLTAGE_CONNECTION',r'voltimetro.{0,60}(conectar|ligar|conexao)'),
]

def run(base,out):
    cross=json.loads((ROOT/'data/acervo-ampliado/cruzamento-35-temas.json').read_text(encoding='utf-8-sig'))['modulos']
    modules={m['modulo']:m for m in cross};topics=collections.defaultdict(list)
    for m in cross:
        for f in m['fontes']:topics[f['id_dossie']].append(m['modulo'])
    current=collections.defaultdict(list);prior_text=collections.defaultdict(list)
    for p in sorted((base/'livros senai/questoes').rglob('*.md')):
        text=p.read_text(encoding='utf-8-sig');head=re.match(r'#\s+(\d+\.\d+)\s+(.+)',text)
        if head:
            for sid in set(re.findall(r'\bQ\d+\b',text)):current[sid].append({'id':head[1],'title':head[2],'file':str(p)})
            for block in re.split(r'^###\s+.+$',text,flags=re.M)[1:]:
                statement=block.split('\n- **')[0].strip()
                statement=re.sub(r'!\[[^\]]*\]\([^)]*\)','',statement)
                if statement:prior_text[norm(statement)].append({'id':head[1],'title':head[2],'file':str(p),'join_method':'EXACT_NORMALIZED_STATEMENT'})
    raw=[];source_files=[]
    for p in sorted((base/'eletrica_eletronica/questoes').glob('lote_*.json')):
        data=p.read_bytes();d=json.loads(data.decode('utf-8-sig'));assert d['total']==len(d['questoes']),p
        raw.extend((q,p.name) for q in d['questoes']);source_files.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'count':len(d['questoes'])})
    ids=[q['codigo'] for q,p in raw];assert len(ids)==len(set(ids)),'Repeated IDs: do not overwrite'
    index=json.loads((base/'eletrica_eletronica/_index.json').read_text(encoding='utf-8-sig'))
    indexids={q['codigo'] for q in index['questoes']};assert set(ids)==indexids,'Index reconciliation failed'
    catalog=[];exact=collections.defaultdict(list);variants=collections.defaultdict(list);imagehash=collections.defaultdict(set)
    for q,file in raw:
        sid=q['codigo'];statement=q.get('enunciado') or '';s=norm(statement);metadata=norm(' '.join(q.get('assuntos',[])))
        alternatives=q.get('alternativas',[]);ct=current[sid] or prior_text.get(s,[]);context=s+' '+metadata
        scores=collections.Counter();reasons=collections.defaultdict(list)
        for tid in ct:
            for m in topics[tid['id']]:scores[m]+=1;reasons[m].append('Prior topic '+tid['id'])
        for m,pattern in RULES.items():
            if match(pattern,s):scores[m]+=4;reasons[m].append('Statement contextual concept: '+pattern)
            elif match(pattern,metadata):scores[m]+=2;reasons[m].append('Subject metadata concept')
        # The word bloqueio alone never maps S01. Hydraulic context needs electric safety evidence.
        if match(r'valvula|hidraul|pneumat',s) and not match(r'nr.?10|desenergiza|ausencia de tensao',s):
            scores.pop('S01',None);reasons.pop('S01',None)
        ranked=sorted(scores,key=lambda m:(-scores[m],m));primary=ranked[0] if ranked else None
        competing=bool(len(ranked)>1 and scores[ranked[1]]==scores[primary])
        confidence='HIGH' if primary and scores[primary]>=5 and not competing else 'MEDIUM' if primary and scores[primary]>=3 and not competing else 'LOW' if primary else 'UNCLASSIFIED'
        images=q.get('imagens',[]);nhtml=len(re.findall(r'<img\b',q.get('enunciado_html') or '',re.I));missing=[];refs=[]
        for im in images:
            rel=im.get('caminho') or ('imagens/'+im['arquivo'] if im.get('arquivo') else None);p=base/'eletrica_eletronica'/rel if rel else None
            valid=bool(p and p.is_file());digest=hashlib.sha256(p.read_bytes()).hexdigest() if valid else None
            refs.append({'path':str(p) if p else None,'exists':valid,'sha256':digest,'source_url':im.get('url_original')})
            if not valid:missing.append(rel)
            if digest:imagehash[digest].add(sid)
        visual=match(r'figura|diagrama|grafico|circuito (abaixo|a seguir)|considere o circuito|circuito apresentado|observe.{0,25}(circuito|imagem)',s)
        visualabsence=visual and not images
        gap=nhtml>len(images)
        image_status='IMAGE_MISSING' if missing or gap or visualabsence else 'IMAGE_ESSENTIAL' if visual and images else 'IMAGE_USEFUL' if images else 'IMAGE_OPTIONAL'
        types=[]
        tf=len(alternatives)==2 and {norm(a.get('texto')) for a in alternatives} in [{'certo','errado'},{'verdadeiro','falso'}]
        multiple=match(r'assertiv|proposic|afirmativas|\bi\s*[.−–-].{0,200}\bii\s*[.−–-]|verdadeiras.{0,20}falsas',s)
        if tf:types.append('TRUE_FALSE')
        if multiple:types.append('MULTIPLE_PROPOSITIONS')
        if match(r'\d\s*(v\b|a\b|ohm|ω|Ω|w\b|hz|kw|ma\b)|calcule|calcular|valor.{0,30}(corrente|tensao|resistencia|potencia)|resistencia equivalente',s):types.append('CALCULATION')
        if match(r'grafico|curva apresentada|curva abaixo',s):types.append('GRAPH')
        if visual or match(r'diagrama|esquema apresentado',s):types.append('DIAGRAM')
        if match(r'procedimento|sequencia|ordem.{0,20}(correta|operac)|desenergiza|reenergiza',s):types.append('PROCEDURE')
        if match(r'\bnr.?\d|nbr|norma.{0,25}(seguranca|regulament)|seguranca do trabalho',s):types.append('SAFETY_NORM')
        if match(r'identifi.{0,30}(componente|simbolo)|componente.{0,20}(representado|ilustrado)',s):types.append('COMPONENT_IDENTIFICATION')
        if match(r'ladder',s):types.append('LADDER_LOGIC')
        if match(r'multimetro|voltimetro|amperimetro|medicao|medir|instrumento de medida',s):types.append('MEASUREMENT')
        if not types:types=['CONCEPTUAL' if s else 'OTHER']
        families=[name for name,pattern,*condition in FAMILIES if match(pattern,s) and (not condition or match(condition[0],s))]
        # Prefer explicit association over the broad Ohm candidate.
        if any(f in families for f in ['PARALLEL_EQUIVALENT_RESISTANCE','SERIES_EQUIVALENT_RESISTANCE']):families=[f for f in families if f!='OHMS_LAW_DIRECT_RESISTANCE']
        family=families[0] if families else None
        formats=[]
        if 'CALCULATION' in types:formats+=['STEP_BY_STEP_CALCULATION','FORMULA_SELECTION','DATA_EXTRACTION','UNIT_SELECTION']
        if tf or multiple:formats+=['TRUE_FALSE_REASONING','ERROR_LOCALIZATION']
        if 'DIAGRAM' in types:formats+=['DIAGRAM_CLICK']
        if 'PROCEDURE' in types:formats+=['SEQUENCE_ORDERING']
        if 'COMPONENT_IDENTIFICATION' in types:formats+=['COMPONENT_SELECTION']
        if match(r'falha|defeito|diagnostico',s):formats+=['FAULT_DIAGNOSIS']
        issues=[]
        if not s:issues.append('MISSING_STATEMENT')
        if len(alternatives)<2:issues.append('INSUFFICIENT_OPTIONS')
        if missing:issues.append('LOCAL_IMAGE_REFERENCE_MISSING')
        if gap:issues.append('HTML_IMAGE_COUNT_GAP')
        if visualabsence:issues.append('VISUAL_CONTEXT_WITHOUT_IMAGE')
        if competing:issues.append('THEMATIC_TIE')
        state='INCOMPLETE' if not s or len(alternatives)<2 else 'NEEDS_INSPECTION' if issues else 'STRUCTURALLY_AVAILABLE'
        potential='LOW' if state=='INCOMPLETE' else 'MEDIUM' if image_status=='IMAGE_MISSING' else 'HIGH' if formats and ('CALCULATION' in types or tf or 'PROCEDURE' in types) else 'MEDIUM' if formats else 'NONE'
        signature=norm(statement)+'|'+json.dumps([(norm(a.get('texto'))) for a in alternatives],ensure_ascii=False)+'|'+str([im.get('url_original') for im in images])
        if s:exact[hashlib.sha256(signature.encode()).hexdigest()].append(sid)
        skeleton=re.sub(r'\d+(?:[.,]\d+)?','<NUMBER>',norm(statement))
        if len(skeleton)>80:variants[skeleton].append(sid)
        r={'source_id':sid,'source_file':file,'source_reference':q.get('link'),'current_theme':q.get('disciplina'),'current_subthemes':q.get('assuntos',[]),'prior_topics':ct,'statement':statement or None,'text_available':bool(s),'alternatives_count':len(alternatives),'has_image':bool(images or nhtml),'image_status':image_status,'image_essential':True if image_status=='IMAGE_ESSENTIAL' else None,'image_essential_confidence':'MEDIUM' if visual else 'LOW','image_references':refs,'html_image_count':nhtml,'probable_types':types,'probable_type':types[0],'preliminary_level':'INTERMEDIATE' if match(r'rlc|fasor|trifas|kirchhoff|intertravamento',s) else 'UNKNOWN','dependencies':['VISUAL_INSPECTION'] if images or visual else [],'structural_state':state,'inspection_reasons':issues,'primary_module':primary,'secondary_modules':ranked[1:],'module_candidates':[{'module':m,'score':scores[m],'relevance':'HIGH' if scores[m]>=5 else 'MEDIUM' if scores[m]>=3 else 'LOW','reasons':reasons[m]} for m in ranked],'theme_classification_confidence':confidence,'semantic_family':family,'secondary_families':families[1:],'family_status':'PRELIMINARY_CONTEXTUAL' if family else 'UNASSIGNED','interaction_candidate':potential,'interaction_formats':list(dict.fromkeys(formats)),'tf_level_candidate':('TF_L4' if tf and match(r'sempre|somente|apenas|obrigatori|qualquer',s) else 'TF_L3' if tf else None),'answer_status':'UNRESOLVED','source_answer_available':q.get('gabarito') is not None,'editorial_decision':'INSPECT' if issues or confidence in ['LOW','UNCLASSIFIED'] else 'CANDIDATE_NOT_VALIDATED'}
        catalog.append(r)
    exactgroups=[v for v in exact.values() if len(v)>1];variantgroups=[v for v in variants.values() if len(v)>1];imagegroups=[sorted(v) for v in imagehash.values() if len(v)>1]
    redundantids=set(x for g in exactgroups+variantgroups for x in g)
    familygroups=collections.defaultdict(list)
    for r in catalog:
        if r['semantic_family']:familygroups[r['semantic_family']].append(r['source_id'])
    save(out/'catalogo-global.json',{'method':'Contextual deterministic preliminary triage v1; no answer generation, no technical certification.','questions':catalog})
    save(out/'familias-semanticas.json',{'method':'Explicit concept patterns; unassigned items are retained, not given fabricated families. Family membership does not prove duplication.','families':dict(familygroups),'unassigned':[r['source_id'] for r in catalog if not r['semantic_family']]})
    save(out/'redundancias-candidatas.json',{'exact_text_options_urls':exactgroups,'numeric_text_variants':variantgroups,'shared_image_hashes':imagegroups,'skill_groups':dict(familygroups),'warning':'Numerical variants and shared figures require review; no deletions. Skill groups alone are not duplicate counts. Semantic paraphrases are not exhaustively detected.'})
    for name,predicate in [('questoes-imagem',lambda r:r['has_image'] or r['image_status']=='IMAGE_MISSING'),('questoes-vf',lambda r:'TRUE_FALSE' in r['probable_types'] or 'MULTIPLE_PROPOSITIONS' in r['probable_types']),('candidatas-interativas',lambda r:r['interaction_candidate']!='NONE'),('pendencias-inspecao',lambda r:r['editorial_decision']=='INSPECT')]:save(out/(name+'.json'),[{'source_id':r['source_id'],'primary_module':r['primary_module'],'types':r['probable_types'],'image_status':r['image_status'],'tf_level':r['tf_level_candidate'],'interaction_candidate':r['interaction_candidate'],'formats':r['interaction_formats'],'reasons':r['inspection_reasons']} for r in catalog if predicate(r)])
    queues=[]
    for mid,m in modules.items():
        rows=[r for r in catalog if any(c['module']==mid for c in r['module_candidates'])]
        bylevel={level:[r['source_id'] for r in rows if next(c['relevance'] for c in r['module_candidates'] if c['module']==mid)==level] for level in ['HIGH','MEDIUM','LOW']}
        queue={'module':mid,'title':m['titulo'],'total_candidates':len(rows),'primary_assignments':sum(r['primary_module']==mid for r in rows),'high_relevance':len(bylevel['HIGH']),'medium_relevance':len(bylevel['MEDIUM']),'low_relevance':len(bylevel['LOW']),'outside_theme':{'count':None,'status':'NOT_SEMANTICALLY_REVIEWED'},'image_dependent':sum(r['image_status'] in ['IMAGE_ESSENTIAL','IMAGE_MISSING'] for r in rows),'possible_duplicates':sum(r['source_id'] in redundantids for r in rows),'possible_semantic_variants':sum(r['source_id'] in {x for g in variantgroups for x in g} for r in rows),'priority_ids':bylevel,'candidate_details':[{'source_id':r['source_id'],'subtopics':[t for t in r['prior_topics'] if mid in topics[t['id']]],'family':r['semantic_family'],'confidence':r['theme_classification_confidence'],'needs_inspection':r['editorial_decision']=='INSPECT'} for r in rows]}
        save(out/'por-modulo'/f'{mid}.json',queue);queues.append({k:v for k,v in queue.items() if k not in ['priority_ids','candidate_details']})
    counts=collections.Counter(t for r in catalog for t in r['probable_types']);classified=sum(r['primary_module'] is not None for r in catalog)
    summary={'TOTAL_QUESTIONS':len(catalog),'INDEX_TOTAL':index['total'],'INDEX_IDS_MATCH':True,'CLASSIFIED':classified,'UNCLASSIFIED':len(catalog)-classified,'WITH_IMAGES':sum(r['has_image'] for r in catalog),'IMAGE_MISSING':sum(r['image_status']=='IMAGE_MISSING' for r in catalog),'TRUE_FALSE':counts['TRUE_FALSE'],'MULTIPLE_PROPOSITIONS':counts['MULTIPLE_PROPOSITIONS'],'CALCULATION':counts['CALCULATION'],'CONCEPTUAL':counts['CONCEPTUAL'],'DIAGRAM':counts['DIAGRAM'],'PROCEDURE':counts['PROCEDURE'],'POSSIBLE_DUPLICATES':len(redundantids),'EXACT_DUPLICATE_GROUPS':len(exactgroups),'NUMERIC_VARIANT_GROUPS':len(variantgroups),'SHARED_IMAGE_GROUPS':len(imagegroups),'HIGH_INTERACTION_POTENTIAL':sum(r['interaction_candidate']=='HIGH' for r in catalog),'MODULE_ASSIGNMENTS':sum(len(r['module_candidates']) for r in catalog),'SEMANTIC_FAMILY_ASSIGNED':sum(bool(r['semantic_family']) for r in catalog),'INSPECTION_QUEUE':sum(r['editorial_decision']=='INSPECT' for r in catalog),'ALL_ANSWERS_UNRESOLVED':all(r['answer_status']=='UNRESOLVED' for r in catalog),'TYPE_COUNTS_MULTI_LABEL':dict(counts),'MODULES':queues,'SOURCE_FILES':source_files,'LIMITS':['Type counts overlap. Module assignments include primary and secondary.','Heuristic contextual triage is not exhaustive semantic reading or difficulty assessment.','Image essentiality is inferred from text, not visual inspection of all images.','No automatic rejection or answer generation. Microlote verification remains separate.']}
    summary['PRIOR_TOPIC_JOINS']=sum(bool(r['prior_topics']) for r in catalog)
    summary['BROKEN_LOCAL_IMAGE_QUESTIONS']=sum('LOCAL_IMAGE_REFERENCE_MISSING' in r['inspection_reasons'] for r in catalog)
    summary['HTML_IMAGE_GAP_QUESTIONS']=sum('HTML_IMAGE_COUNT_GAP' in r['inspection_reasons'] for r in catalog)
    summary['VISUAL_CONTEXT_WITHOUT_IMAGE']=sum('VISUAL_CONTEXT_WITHOUT_IMAGE' in r['inspection_reasons'] for r in catalog)
    summary['MISSING_STATEMENTS']=sum(not r['text_available'] for r in catalog)
    save(out/'resumo-global.json',summary)
    assert classified+summary['UNCLASSIFIED']==len(ids)==index['total']
    assert len(queues)==35 and all(r['answer_status']=='UNRESOLVED' for r in catalog)
    lines=['# Varredura global do acervo','', 'Todas as questões dos lotes foram percorridas e reconciliadas com o índice. Nenhum gabarito foi gerado, nenhuma questão publicada e nenhum arquivo externo alterado.','', '**Limite:** classificação contextual automatizada e preliminar. Combina enunciados, assuntos e tópicos anteriores, sem afirmar leitura semântica individual certificada. Casos incertos são mantidos na fila de inspeção; não foram rejeitados automaticamente.','', '| Indicador | Total |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in summary.items() if isinstance(v,(int,bool))]
    lines += ['', 'Tipos são multilabel: não somar CALCULATION, DIAGRAM, MEASUREMENT etc. CLASSIFIED indica módulo candidato, não pertinência tecnicamente validada. MODULE_ASSIGNMENTS inclui secundários. POSSIBLE_DUPLICATES conta IDs em grupos exatos ou variantes numéricas de texto, não grupos de habilidade. Imagens ausentes incluem referências locais quebradas, lacunas HTML e contexto visual sem imagem; as causas podem se sobrepor.','', '## Filas dos 35 módulos','', '| Módulo | Candidatas | Fortes | Médias | Fracas | Imagem | Redundância candidata |','|---|---:|---:|---:|---:|---:|---:|']
    lines += [f"| [{q['module']}](../data/acervo-ampliado/por-modulo/{q['module']}.json) | {q['total_candidates']} | {q['high_relevance']} | {q['medium_relevance']} | {q['low_relevance']} | {q['image_dependent']} | {q['possible_duplicates']} |" for q in queues]
    lines += ['', '## Critérios e próximos passos','', 'As pontuações são regras de triagem, não probabilidades: conceito contextual no enunciado soma 4, assunto registrado soma 2 e tema anterior soma 1. HIGH exige pelo menos 5 sem empate; MEDIUM exige 3; empates e sinais fracos ficam LOW. Válvula/hidráulica sem contexto de segurança elétrica não entram em S01 pelo termo bloqueio.','', 'Famílias usam relações conceituais explícitas. Itens não cobertos permanecem UNASSIGNED. Variantes numéricas são agrupadas pelo enunciado normalizado; paráfrases semânticas não são detectadas exaustivamente. Figuras iguais são agrupadas por hash sem supor que suas questões sejam iguais.','', 'A dificuldade é UNKNOWN, salvo sinal preliminar INTERMEDIATE em conceitos como RLC e intertravamento; não foi calibrada por desempenho. V/F usa texto das duas opções Certo/Errado ou Verdadeiro/Falso. TF_L3/TF_L4 são sugestões provisórias; não foram criadas etapas. Imagem indispensável nunca é certificada automaticamente. Fora do tema tem contagem nula, pois requer revisão e não deve ser inventado como zero.','', 'Reexecutar: `python scripts/catalogar-acervo-global.py`. Os hashes dos 49 lotes ficam em resumo-global.json. Os índices são externos ao bundle. Começar a revisão editorial pela fila S01, incluindo candidatos fracos e itens sem classificação; depois resolver, conferir e adaptar apenas o subconjunto revisado. Não começar publicação nem preencher os 9.791 gabaritos.','']
    (ROOT/'docs/11-varredura-global-acervo.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if isinstance(v,(int,bool))},ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',type=Path,default=Path(r'C:\dev\extrator de perguntas'));parser.add_argument('--out',type=Path,default=ROOT/'data/acervo-ampliado');args=parser.parse_args();run(args.base,args.out)
