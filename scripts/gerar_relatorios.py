from pathlib import Path
import collections, hashlib, json, re
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/extraidos'
def load(name):return json.loads((OUT/(name+'.json')).read_text(encoding='utf8'))
docs=[load(x) for x in ['avaliacoes','avaliacoes-2','simulado-2026']]
summary=load('resumo')
unique=load('indice-deduplicado')['itens']
themes=sorted(set(i['tema_principal'] for d in docs for i in d['itens']))
counts=[collections.Counter(i['tema_principal'] for i in d['itens']) for d in docs]
uc=collections.Counter(i['tema_principal'] for i in unique)
table='| Tema principal | avaliações | avaliações 2 | Simulado 2026 | Itens distintos |\n|---|---:|---:|---:|---:|\n'+'\n'.join(f'| {t} | {counts[0][t]} | {counts[1][t]} | {counts[2][t]} | {uc[t]} |' for t in themes)
types=['conceitual','cálculo','leitura de diagrama','norma e segurança']
tc=[collections.Counter(i['tipo_principal'] for i in d['itens']) for d in docs]
typetable='| Tipo principal | avaliações | avaliações 2 | Simulado 2026 |\n|---|---:|---:|---:|\n'+'\n'.join(f'| {t} | {tc[0][t]} | {tc[1][t]} | {tc[2][t]} |' for t in types)
fig=[sum(i['possui_figura'] for i in d['itens']) for d in docs]
text=f'''# Fase 0 - Diagnóstico das provas do workspace

Data: 02/10/2026. Escopo: os três PDFs da raiz; não havia apostilas ou anotações adicionais no workspace. Originais preservados. Plano de trabalho: `PLANO-DE-EXECUCAO.md`.

## Identificação e premissas

| Arquivo | Páginas | Itens | Curso / evidência | Ano | Gabarito |
|---|---:|---:|---|---|---|
| avaliações.pdf | 40 | 40 | Técnico em Eletrotécnica, ficha na p. 40 | Não informado | 40 respostas, pp. 39-40 |
| avaliações 2.pdf | 37 | 40 | Técnico em Eletrotécnica, ficha na p. 37 | Não informado | 40 respostas, pp. 36-37 |
| SIMULADO 2026.pdf | 32 | 41 | Enunciados de Eletrotécnica; sem ficha de curso | 2026 no nome; impressão 20/05/26 | Não encontrado |

Os dois primeiros mostram SENAI/SisBia e IDs SAEP, matriz **versão 1** e itinerário **2022**. O campo “Ano de Aplicação da Matriz” está em branco. Não confundir 2022 com ano da prova, nem versão 1 com o conteúdo integral da Matriz de Referência. A origem local e os logotipos não comprovam que sejam cadernos efetivamente aplicados em uma edição nacional. Portanto, a premissa “três provas anteriores do SAEP” precisa de ajuste: são **duas avaliações locais com gabarito e um simulado**, com aplicação oficial não comprovada. Não há indicação de outro curso que exija interromper o diagnóstico.

## Extração, rastreabilidade e qualidade

Texto nativo extraído com PyMuPDF; OCR não foi necessário nos três documentos. JSONs: `data/extraidos/avaliacoes.json`, `avaliacoes-2.json` e `simulado-2026.json`. Cada item registra ID, ordem, página(s), enunciado, quatro alternativas, gabarito ou `null`, tema/tipo editorial e referências a figuras com página e coordenadas. O texto de todas as páginas também está preservado em JSON e TXT. URLs administrativas do Forms foram omitidas nas extrações; não foram abertas.

Diagramas, placas, fórmulas e tabelas em imagem foram salvos em `data/extraidos/figuras/`. O conteúdo dessas imagens não foi inventado como texto: descrição acessível e interpretação técnica estão marcadas [VERIFICAR]. Algumas alternativas são exclusivamente gráficas; letras A-D sem texto são esperadas nesses casos. Em cinco itens do Forms, A/B e C/D estão em duas colunas; a extração os separa em quatro alternativas. As letras do Forms foram atribuídas pela ordem visual; não são gabarito.

Leitura textual dos itens e conferência visual de páginas com cabeçalho, circuito, alternativas gráficas, gabarito e metadados. Verificação estrutural completa de contagem, letras e correspondência do gabarito. Isso não é revisão técnica integral das respostas.

## Formato e figuras

Enunciados contextualizados em serviços industriais/prediais, situação-problema, comando curto e **quatro alternativas** com uma resposta indicada nos gabaritos dos dois primeiros. A folha genérica de respostas inclui coluna E, mas os itens têm A-D. Não adotar cinco alternativas por causa dessa folha.

Há questões divididas entre páginas; nem página nem cabeçalho “Pagina 1 de 1” equivalem a um item. O simulado tem capa, numeração de 1 a 41, botões de escolha e rodapé do Forms. Não mostra cronômetro, pontuação nem respostas certas.

Itens com pelo menos uma imagem técnica detectada (logotipos excluídos): **{fig[0]}/40**, **{fig[1]}/40** e **{fig[2]}/41**. Incluem diagramas elétricos/Ladder/pneumáticos, placas, tabelas, formas de onda, estruturas de distribuição e equações. “Ter figura” e “leitura de diagrama” são métricas diferentes: cálculos e questões normativas também usam imagens.

## Tipos de item

{typetable}

Classificação manual pelo procedimento principal para responder: cálculo quando precisa operar valores (mesmo com tabela/placa); leitura de diagrama quando precisa interpretar conexões, símbolos ou sequência; norma e segurança quando a exigência/procedimento normativo é central; conceitual nos demais. São categorias exclusivas para contagem; itens podem mobilizar várias competências. Não são códigos oficiais da matriz.

## Distribuição por tema

{table}

Totais: 40 + 40 + 41 = **121 ocorrências**. Os dois arquivos de avaliações têm **33 IDs em comum**, sem divergência das letras dos respectivos gabaritos; restam **47 IDs SAEP distintos**. O simulado repete exatamente o enunciado/opções das questões **10 e 23**, inclusive a figura. São **40 itens distintos** nesse documento. Índice conservador: **87 itens**, em `indice-deduplicado.json`; ocorrências e proveniência continuam preservadas nos arquivos individuais. Não removemos questões apenas porque têm o mesmo tema. Arquivos PDF não são duplicatas binárias; SHA-256 no manifesto.

Frequências descrevem esta pequena coleção local, não a probabilidade de cair na próxima prova. Não somar os dois cadernos como amostras independentes. A Fase 2 deverá usar também a frequência deduplicada, os pré-requisitos e a matriz oficial, quando disponível.

## Padrões de distratores observados

| Padrão | Evidência local | Implicação para questões originais |
|---|---|---|
| Troca de grandeza, unidade ou operação | SAEP_76385 mistura resistência com resultado de P/V e produtos/inversões; SAEP_77826 troca sentido da relação de transformação e escala V/kV | Gerar distratores pela operação incorreta e explicar a unidade |
| Total versus parte | SAEP_77683 fala em corrente por tomada, mas alternativas/gabarito indicam corrente do conjunto | Corrigir a redação original; não perpetuar ambiguidade |
| Troca de escala e modo de conexão | SAEP_77411; SAEP_78272; SIM2026_10/23; SIM2026_40 | Distinguir CA/CC, corrente/tensão/continuidade e conexão apropriada |
| Ordem insegura ou etapa omitida | SAEP_78307, SAEP_77014, SAEP_78432 | Avaliar sequência e consequência sem transformar distrator em orientação |
| Tecnologia/dispositivo de função parecida | SAEP_77568, SAEP_77578, SIM2026_32 | Contrastar finalidade de soft-starter/inversor e das proteções |
| Relação CA/CC e blocos do inversor | SAEP_76953, SAEP_76121, SAEP_76352 | Explorar sentido da corrente, retificação/inversão e relação V/f |
| Topologia/lógica semelhante | SAEP_76509, SAEP_78273, SAEP_78287, SAEP_77858; SIM2026_34 | Trocar selo/intertravamento, AND/OR, entradas/saídas e sequência de atuadores |
| Símbolos e leitura de catálogo | SIM2026_08/19/29/41 | Criar figuras próprias com diferenças interpretáveis |

Esses padrões são leitura editorial das opções; não há dados de respostas de alunos para medir quais erros são mais frequentes. Esquecer √3/rendimento é uma hipótese do pedido, não um padrão universal comprovado por estes itens.

## Alertas técnicos e lacunas [VERIFICAR]

- **SAEP_77683**: 250 W / 220 V ≈ 1,14 A por tomada; quatro tomadas dão ≈ 4,55 A no total (hipótese resistiva implícita do item). O gabarito B aponta 4,5 A apesar do comando “cada tomada”. Preservado como fonte, sinalizado para não virar regra de ensino.
- **SIM2026_06**: oferece “3 e 4”, embora só enumere três objetivos. Revisar redação e fonte antes de gerar item original.
- **SIM2026_18**: descreve conjuntamente proteção contra fuga, sobrecarga e curto-circuito, mas oferece “DR” sem distinguir IDR de DDR. Revisar com catálogo e norma; não atribuir gabarito inferido.
- **SAEP_77817**: afirma um limite de 5 cv para concessionárias. [VERIFICAR] em norma da concessionária relevante; não usar como limite nacional universal.
- **SAEP_78480 / SIM2026_20/21/22**: não transportar fatores, seção ou disjuntor para regra geral; verificar método de instalação, condutores carregados, temperatura, agrupamento e coordenação de proteção.
- **SAEP_76652**: verificar contexto CA/CC antes de generalizar o valor de 49 V da fonte; a letra extraída não substitui a definição normativa.
- **Laboratório solicitado**: conferir a sequência completa de desenergização na NR-10, além das três etapas citadas no pedido; conferir a técnica de identificação de polaridade das bobinas, pois o item SAEP_78454 trata apenas de continuidade/pares. [VERIFICAR] antes da implementação.
- A coleção não comprova cobertura de motores de 9/12 pontas ou Dahlander, nem de todas as matérias do curso. Ausência aqui não significa exclusão do currículo ou da prova.

## Resumo da Fase 0 (8 linhas)

1. Três PDFs localizados; conteúdo compatível com Técnico em Eletrotécnica.
2. Duas avaliações SisBia com 40 itens cada; um simulado com 41.
3. Dois gabaritos completos extraídos; simulado sem gabarito.
4. Ano das avaliações não informado; itinerário 2022 não é ano de aplicação.
5. Texto/itens/alternativas/figuras estruturados e rastreáveis por página.
6. 33 IDs comuns e uma repetição no simulado: 87 itens distintos conservadores.
7. Distribuição, tipos e padrões de distratores registrados; ambiguidades marcadas.
8. Diagnóstico encerrado; seguimos para a coleta da Fase 1, sem iniciar o app.
'''
(ROOT/'docs/00-diagnostico.md').write_text(text,encoding='utf8')

class Plain(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style'):self.skip=max(0,self.skip-1)
    def handle_data(self,s):
        if not self.skip and s.strip():self.parts.append(s.strip())
for path in (ROOT/'data/provas').glob('*.html'):
    parser=Plain();parser.feed(path.read_text(encoding='utf8',errors='replace'))
    plain='\n'.join(parser.parts)
    (OUT/(path.stem+'.txt')).write_text(plain,encoding='utf8')
    (OUT/(path.stem+'.json')).write_text(json.dumps({'fonte':path.relative_to(ROOT).as_posix(),'texto':plain},ensure_ascii=False,indent=2),encoding='utf8')

# Verificações dos dados, não testes de um aplicativo ainda inexistente.
checks=[]
for d in docs:
    assert len(d['itens'])==d['numero_itens']
    assert len({i['id'] for i in d['itens']})==d['numero_itens']
    assert all([a['letra'] for a in i['alternativas']]==list('ABCD') for i in d['itens'])
    assert all(i['enunciado'].strip() for i in d['itens'])
    assert all((ROOT/f['arquivo']).exists() for i in d['itens'] for f in i['figuras'])
    if d['arquivo_origem'].startswith('avaliações'):
        assert all(i['gabarito']['resposta'] in 'ABCD' for i in d['itens'])
    else:assert all(i['gabarito']['resposta'] is None for i in d['itens'])
    checks.append({'arquivo':d['arquivo_origem'],'itens':len(d['itens']),'alternativas':'4 por item, A-D','gabaritos':sum(i['gabarito']['resposta'] is not None for i in d['itens']),'figuras_referenciadas':sum(len(i['figuras']) for i in d['itens']),'status':'OK'})
assert summary['total_ocorrencias']==121 and len(unique)==87
assert len(summary['duplicatas_por_id'])==33
assert all(len({o['resposta'] for o in dup['ocorrencias']})==1 for dup in summary['duplicatas_por_id'])
manifest=json.loads((ROOT/'data/provas/manifesto.json').read_text(encoding='utf8'))
for e in manifest['documentos']:
    if e.get('arquivo'):
        assert hashlib.sha256((ROOT/e['arquivo']).read_bytes()).hexdigest()==e['sha256']
(ROOT/'docs/verificacao-fases-0-1.json').write_text(json.dumps({'data':'2026-10-02','checks':checks,'ocorrencias':121,'itens_distintos':87,'ids_compartilhados':33,'gabaritos_compartilhados':'sem divergência','hashes':'todos os arquivos presentes conferem com manifesto','limite':'Verificação estrutural; revisão técnica e transcrição acessível de figuras pendentes.'},ensure_ascii=False,indent=2),encoding='utf8')
print('Relatório e verificação gerados. 121 ocorrências; 87 itens distintos; hashes OK.')
