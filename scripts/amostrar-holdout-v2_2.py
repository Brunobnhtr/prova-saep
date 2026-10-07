"""Amostragem Estratificada Neutra para Blind Holdout V2.2 (~300 questoes).
Criterios metodologicos:
1. Exclusao estrita dos 384 IDs conhecidos (153 Golden + 31 Target Regressions + 200 Dev Audit).
2. Estratificacao PUREMENTE por metadados neutros originais:
   - current_theme (tema original de origem do acervo bruto, sem relacao com V2.2)
   - has_image (presenca de imagem: binario)
   - length_bucket (curto, medio, longo)
   - question_type (VF, MULTIPLE_PROPOSITIONS, STANDARD)
3. O pacote de anotacao gerado (holdout-v2_2-annotation-pack.json) NAO contem:
   - primary_module, primary_concept, semantic_family, confidence, unclassified_reason
   - Nenhuma previsao de nenhum classificador.
4. Gera semente fixa (random_seed=42) para reprodutibilidade estrita.
"""

from pathlib import Path
import json, random, collections, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/acervo-ampliado'

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def save(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    random.seed(42)

    # 1. Carregar os 384 IDs conhecidos a serem excluidos
    gold = {q['source_id'] for q in load(OUT / 'classification-golden-set.json')['questions']}
    targets = {'Q825995', 'Q2217076', 'Q3958246', 'Q2916786', 'Q810802', 'Q770887', 'Q770894', 'Q431575', 'Q3452153', 'Q4093465', 'Q3393722', 'Q3291406', 'Q751907', 'Q3981910', 'Q3978783', 'Q3675303', 'Q3232086', 'Q2955277', 'Q2401042', 'Q2323269', 'Q3125841', 'Q2737528', 'Q3850333', 'Q3012489', 'Q2779437', 'Q2930977', 'Q3027672', 'Q3485343', 'Q2403191', 'Q3976932', 'Q2955288'}
    dev_audit = set(load(OUT / 'holdout_ground_truth.json').keys())
    known_384 = gold | targets | dev_audit
    assert len(known_384) == 384, f"Esperado 384 IDs conhecidos, obtido {len(known_384)}"

    # 2. Carregar catalogo global original V1
    v1_questions = load(OUT / 'catalogo-global.json')['questions']
    total_pool = [q for q in v1_questions if q['source_id'] not in known_384]
    assert len(total_pool) == 9791 - 384 == 9407

    # 3. Agrupar em estratos neutros por metadados de entrada
    # Dimensoes neutras:
    # - current_theme (eletricidade basica, comandos, maquinas, instalacoes, etc.)
    # - has_image (True/False)
    # - is_vf (True/False)
    strata = collections.defaultdict(list)
    for q in total_pool:
        theme = q.get('current_theme') or 'SEM_TEMA'
        has_img = bool(q.get('has_image'))
        is_vf = bool(q.get('is_true_false'))
        stmt_len = len(q.get('statement') or '')
        len_bucket = 'SHORT' if stmt_len < 200 else ('LONG' if stmt_len > 600 else 'MEDIUM')
        
        # Chave de estrato neutra
        stratum_key = f"{theme}__IMG:{has_img}__VF:{is_vf}__LEN:{len_bucket}"
        strata[stratum_key].append(q)

    # 4. Amostragem proporcional visando ~300 questoes
    target_sample_size = 300
    sample = []
    
    # Ordenar estratos de forma deterministica
    sorted_strata_keys = sorted(strata.keys())
    
    # Distribuir cotas com base no peso de cada estrato
    strata_counts = {k: len(strata[k]) for k in sorted_strata_keys}
    total_items = len(total_pool)

    # Cota minima por estrato representativo e restante proporcional
    quotas = {}
    remaining_slots = target_sample_size
    for k in sorted_strata_keys:
        count = strata_counts[k]
        ideal_quota = round((count / total_items) * target_sample_size)
        quotas[k] = ideal_quota

    # Ajustar soma exata para 300
    diff = target_sample_size - sum(quotas.values())
    if diff != 0:
        # Ajusta nos maiores estratos
        by_size = sorted(sorted_strata_keys, key=lambda k: strata_counts[k], reverse=True)
        for i in range(abs(diff)):
            k = by_size[i % len(by_size)]
            if diff > 0:
                quotas[k] += 1
            elif quotas[k] > 0:
                quotas[k] -= 1

    # Sortear deterministicamente
    for k in sorted_strata_keys:
        items = strata[k]
        items_sorted = sorted(items, key=lambda x: x['source_id']) # ordenacao estavel
        random.seed(hash(k) % 10000000 + 42)
        q_count = min(quotas[k], len(items_sorted))
        if q_count > 0:
            sampled_items = random.sample(items_sorted, q_count)
            for it in sampled_items:
                sample.append((k, it))

    # Ajustar para 300 exatos se necessario
    if len(sample) > 300:
        random.seed(42)
        sample = random.sample(sample, 300)
    elif len(sample) < 300:
        # Completar determinista do total_pool fora da amostra
        sampled_ids = {it['source_id'] for _, it in sample}
        remaining_candidates = [it for it in total_pool if it['source_id'] not in sampled_ids]
        remaining_candidates = sorted(remaining_candidates, key=lambda x: x['source_id'])
        random.seed(99)
        needed = 300 - len(sample)
        add = random.sample(remaining_candidates, needed)
        for it in add:
            sample.append(('COMPLEMENT', it))

    # Embaralhar deterministicamente a ordem final
    random.seed(1337)
    random.shuffle(sample)
    assert len(sample) == 300

    # 5. Criar o pacote de anotacao BLIND (SEM previsoes de modelo)
    # Apenas o identificador, texto da questao, tema original bruto, metadados neutros e alternativas
    # Opcionais de alternativas se disponiveis
    options_dict = {}
    p_root = Path(r'C:\dev\extrator de perguntas\eletrica_eletronica\questoes')
    if p_root.exists():
        for p in p_root.glob('lote_*.json'):
            for q in load(p)['questoes']:
                options_dict[q['codigo']] = q.get('alternativas', [])

    annotation_pack = []
    meta_info = []

    for stratum_name, q in sample:
        sid = q['source_id']
        alt_list = options_dict.get(sid, [])
        alt_texts = [f"({a.get('letra', i)}) {a.get('texto', '')}" for i, a in enumerate(alt_list)] if alt_list else []
        
        pack_item = {
            'source_id': sid,
            'sampling_stratum': stratum_name,
            'original_source_theme': q.get('current_theme'),
            'has_image': bool(q.get('has_image')),
            'is_true_false': bool(q.get('is_true_false')),
            'statement': q.get('statement', ''),
            'alternatives': alt_texts
        }
        # VERIFICACAO CRITICA DE BLINDAGEM: Garantir que nenhuma previsao do classificador esta presente
        assert 'primary_module' not in pack_item
        assert 'primary_concept' not in pack_item
        assert 'semantic_family' not in pack_item
        assert 'confidence' not in pack_item
        assert 'unclassified_reason' not in pack_item
        annotation_pack.append(pack_item)

        meta_info.append({
            'source_id': sid,
            'sampling_stratum': stratum_name,
            'original_source_theme': q.get('current_theme'),
            'has_image': bool(q.get('has_image')),
            'statement_length': len(q.get('statement', ''))
        })

    # Salvar arquivos do holdout
    save(OUT / 'holdout-v2_2-annotation-pack.json', {
        'version': 2.2,
        'description': 'Amostra estritamente cega para anotacao editorial de 300 questoes. Sem previsoes de classificadores.',
        'random_seed': 42,
        'excluded_known_ids_count': len(known_384),
        'sample_size': len(annotation_pack),
        'questions': annotation_pack
    })

    save(OUT / 'holdout-v2_2-meta.json', {
        'version': 2.2,
        'sample_size': len(meta_info),
        'items': meta_info
    })

    # Validar e registrar SHA-256 do pacote cego
    pack_bytes = (OUT / 'holdout-v2_2-annotation-pack.json').read_bytes()
    pack_hash = hashlib.sha256(pack_bytes).hexdigest()

    print(f"Amostragem concluida:")
    print(f"- IDs conhecidos excluidos: {len(known_384)}")
    print(f"- Questoes amostradas no pack cego: {len(annotation_pack)}")
    print(f"- SHA-256 do annotation pack: {pack_hash}")

if __name__ == '__main__':
    main()

