import {describe,it,expect} from 'vitest';
import {readFileSync} from 'node:fs';
import {MODULES,getAvailableModules,isModuleUnlocked} from '../src/data/modules';
import {parseStudyState,loadStudyState,saveStudyState,STORAGE_KEY,BACKUP_KEY,emptyState,validateModuleGraph,canStartModule} from '../src/domain/study';
const record={moduleId:'S01',status:'completed',score:80,questionsCompleted:10,questionsCorrect:8,attempts:10,hintsUsed:0,reviewQueue:[],startedAt:'2026-10-06T12:00:00.000Z'};
describe('Trilha real e critérios de acesso',()=>{
 it('corresponde aos 35 temas, ordem, pré-requisitos, prioridade e metas da coleta',()=>{
  const map=JSON.parse(readFileSync(new URL('../../data/fase2/mapa-conteudo.json',import.meta.url),'utf8'));
  expect(MODULES.map(m=>m.id)).toEqual(map.trilha);expect(MODULES).toHaveLength(35);expect(validateModuleGraph(MODULES)).toEqual([]);
  for(const module of MODULES){const entry=map.subtemas.find((m:{id:string})=>m.id===module.id);expect(module.prerequisites).toEqual(entry.pre_requisitos);expect(module.targetQuestions).toBe(entry.meta_questoes_originais);expect(module.priority).toBe(entry.prioridade_frequencia_x_dificuldade);expect(module.order).toBe(map.trilha.indexOf(module.id)+1);}
  expect(MODULES.reduce((sum,m)=>sum+m.targetQuestions,0)).toBe(542);
 });
 it('desbloqueia apenas com todos os requisitos e distingue publicação de elegibilidade',()=>{
  expect(getAvailableModules([]).map(m=>m.id)).toEqual(['S01','F01']);expect(isModuleUnlocked('S02',[])).toBe(false);expect(isModuleUnlocked('S02',['S01'])).toBe(true);expect(isModuleUnlocked('E02',['E01'])).toBe(false);expect(isModuleUnlocked('E02',['E01','M02'])).toBe(true);expect(isModuleUnlocked('XXX',[])).toBe(false);
  expect(MODULES.every(m=>!canStartModule(m.id,MODULES.map(m=>m.id),MODULES))).toBe(true);
 });
 it('detecta ciclos, IDs duplicados, requisitos ausentes e ordem inválida',()=>{
  const a={...MODULES[0],prerequisites:['S02']},b={...MODULES[1],prerequisites:['S01']};expect(validateModuleGraph([a,b]).some(e=>e.includes('Ciclo'))).toBe(true);expect(validateModuleGraph([a,a]).some(e=>e.includes('duplicado'))).toBe(true);expect(validateModuleGraph([{...a,prerequisites:['UNKNOWN']}]).some(e=>e.includes('inexistente'))).toBe(true);
 });
});
describe('Dados locais não são prova de conclusão',()=>{
 it('recupera migração sem confiar em conclusões legadas e conserva datas serializadas',()=>{
  const data=parseStudyState(JSON.stringify({S01:record}),MODULES,true);expect(data.state.progress.S01.status).toBe('in_progress');expect(data.state.progress.S01.startedAt).toBe(record.startedAt);expect(data.notice).toContain('não têm avaliação');
 });
 it('recusa JSON corrompido, versão desconhecida, IDs falsos, NaN, contadores e chaves divergentes',()=>{
  expect(parseStudyState('{',MODULES).state).toEqual(emptyState());expect(parseStudyState(JSON.stringify({version:99,progress:{},savedModules:[]}),MODULES).notice).not.toBe('');
  for(const bad of [{...record,moduleId:'F01'},{...record,questionsCorrect:11},{...record,attempts:-1},{...record,score:101},{...record,reviewQueue:'x'},{...record,questionsCompleted:1.5}])expect(parseStudyState(JSON.stringify({version:1,progress:{S01:bad},savedModules:['S01','S01','FAKE']}),MODULES).state.progress).toEqual({});
 });
 it('deduplica salvos, bloqueia IDs desconhecidos e restaura favoritos',()=>{
  const parsed=parseStudyState(JSON.stringify({version:1,progress:{},savedModules:['S01','S01','FAKE','F01']}),MODULES);expect(parsed.state.savedModules).toEqual(['S01','F01']);
  const values=new Map<string,string>();const storage={getItem:(key:string)=>values.get(key)??null,setItem:(key:string,value:string)=>{values.set(key,value);}};expect(saveStudyState(storage,parsed.state)).toBe('');expect(loadStudyState(storage,MODULES).state).toEqual(parsed.state);
 });
 it('tolera storage indisponível e preserva conteúdo anterior antes de escrever',()=>{
  const broken={getItem:()=>{throw Error('blocked');},setItem:()=>{throw Error('quota');}};expect(loadStudyState(broken,MODULES).notice).not.toBe('');expect(saveStudyState(broken,emptyState())).not.toBe('');
  const values=new Map([[STORAGE_KEY,'{bad']]);const storage={getItem:(key:string)=>values.get(key)??null,setItem:(key:string,value:string)=>{values.set(key,value);}};saveStudyState(storage,emptyState());expect(values.get(BACKUP_KEY)).toBe('{bad');
 });
});
