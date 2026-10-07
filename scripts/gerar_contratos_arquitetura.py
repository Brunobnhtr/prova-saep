"""Contratos documentais da Fase 3; não cria ou executa aplicação."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/arquitetura'
(BASE/'schemas').mkdir(exist_ok=True);(BASE/'exemplos').mkdir(exist_ok=True)
string={'type':'string','minLength':1}
strings={'type':'array','items':string,'uniqueItems':True}
def obj(props,required=None):
    return {'type':'object','additionalProperties':False,'properties':props,'required':required if required is not None else list(props)}
def schema(title,properties):
    return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':title,**obj(properties)}
source=obj({'id':string,'title':string,'locator':string,'verificationStatus':{'enum':['pendente','verificada']}})
module=schema('Contrato de módulo de estudo',{
 'schemaVersion':{'const':1},'id':string,'contentVersion':string,'title':string,'subthemeIds':strings,'prerequisites':strings,
 'matrixItemId':{'type':['string','null']},'matrixStatus':{'enum':['pendente','confirmada']},'technicalStatus':{'enum':['rascunho','revisado']},
 'sources':{'type':'array','items':source},'lessons':{'type':'array','items':obj({'id':string,'markdownPath':string,'sourceIds':strings})},
 'labs':{'type':'array','items':obj({'id':string,'scenarioId':string,'family':string,'sourceIds':strings})},'questionTemplates':strings})
module['allOf']=[{'if':{'properties':{'matrixStatus':{'const':'confirmada'}}},'then':{'properties':{'matrixItemId':string}}}]
template=schema('Contrato de template de questão',{
 'schemaVersion':{'const':1},'id':string,'templateVersion':string,'subthemeId':string,'kind':{'enum':['etapas','simulado']},
 'generatorId':string,'parameterBounds':{'type':'object','additionalProperties':obj({'min':{'type':'number'},'max':{'type':'number'},'unit':string})},
 'optionCount':{'enum':[4,5]},'sourceIds':strings,'technicalStatus':{'enum':['rascunho','revisado']}})
template['allOf']=[{'if':{'properties':{'kind':{'const':'etapas'}}},'then':{'properties':{'optionCount':{'const':4}}}}]
attempt=obj({'id':string,'instanceId':string,'stepId':string,'selectedOptionId':string,'correct':{'type':'boolean'},'hints':{'type':'integer','minimum':0},'attemptIndex':{'type':'integer','minimum':1},'occurredAt':{'type':'string','format':'date-time'}})
instance=obj({'id':string,'templateId':string,'templateVersion':string,'generatorVersion':string,'seed':string,'parameters':{'type':'object','additionalProperties':{'type':'number'}},'optionPermutation':{'type':'array','items':string,'uniqueItems':True}})
review=obj({'subthemeId':string,'dueAt':{'type':'string','format':'date-time'},'intervalDays':{'type':'integer','minimum':0},'lapses':{'type':'integer','minimum':0},'schedulerVersion':string})
session=obj({'id':string,'profileId':string,'startedAt':{'type':'string','format':'date-time'},'deadlineAt':{'type':'string','format':'date-time'},'status':{'enum':['em_andamento','entregue','expirado']},'instanceIds':strings,'answers':{'type':'object','additionalProperties':string}})
backup=schema('Contrato de backup de progresso',{'schemaVersion':{'const':1},'exportedAt':{'type':'string','format':'date-time'},'moduleVersions':{'type':'object','additionalProperties':string},'instances':{'type':'array','items':instance},'attempts':{'type':'array','items':attempt},'reviews':{'type':'array','items':review},'sessions':{'type':'array','items':session}})
schemas={'modulo.schema.json':module,'questao-template.schema.json':template,'progresso.schema.json':backup}
example={'schemaVersion':1,'id':'motores','contentVersion':'0.1.0-draft','title':'Motores elétricos','subthemeIds':['E01','E02','E03','E04','E05','E06'],'prerequisites':['S01','S02','F01','F02','F03','F04','M01','M02','P02'],'matrixItemId':None,'matrixStatus':'pendente','technicalStatus':'rascunho','sources':[{'id':'apoio-comandos','title':'Comandos Elétricos - livro SENAI fornecido pelo usuário','locator':'livro-007; capítulo/edição técnica [VERIFICAR]','verificationStatus':'pendente'}],'lessons':[],'labs':[],'questionTemplates':[]}
for name,value in schemas.items():(BASE/'schemas'/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'exemplos/modulo-motores.json').write_text(json.dumps(example,ensure_ascii=False,indent=2),encoding='utf-8')
print('3 schemas e exemplo documental gerados.')
