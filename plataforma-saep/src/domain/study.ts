import type {Module, UserProgress} from '../types';
export const STORAGE_KEY='saep.study.v1';
export const BACKUP_KEY='saep.study.v1.previous';
export interface StudyState {version:1;progress:Record<string,UserProgress>;savedModules:string[]}
export interface StoragePort {getItem(key:string):string|null;setItem(key:string,value:string):void}
export const emptyState=():StudyState=>({version:1,progress:{},savedModules:[]});
const object=(value:unknown):value is Record<string,unknown>=>typeof value==='object'&&value!==null&&!Array.isArray(value);
const count=(v:unknown)=>Number.isSafeInteger(v)&&Number(v)>=0;
function date(v:unknown){return typeof v==='string'&&/^\d{4}-\d{2}-\d{2}T/.test(v)&&Number.isFinite(Date.parse(v))?v:undefined;}
export function parseStudyState(raw:string,modules:readonly Module[],legacy=false):{state:StudyState;notice:string}{
 const state=emptyState();let notice='';
 if(raw.length>1_000_000)return {state,notice:'O registro local excede o limite de leitura. Os dados originais foram preservados.'};
 let data:unknown;try{data=JSON.parse(raw);}catch{return {state,notice:'O registro local está inválido. A trilha abriu sem carregá-lo; os dados originais foram preservados.'};}
 if(!object(data)||(!legacy&&(data.version!==1||!object(data.progress)||!Array.isArray(data.savedModules))))return {state,notice:'Formato de progresso desconhecido. Os dados originais foram preservados.'};
 const ids=new Set(modules.map(m=>m.id));
 const progress=legacy?data:data.progress as Record<string,unknown>;
 for(const [id,value] of Object.entries(progress)){
  if(!ids.has(id)||!object(value)||value.moduleId!==id||!['in_progress','completed'].includes(String(value.status))||!['questionsCompleted','questionsCorrect','attempts','hintsUsed'].every(k=>count(value[k]))||typeof value.score!=='number'||!Number.isFinite(value.score)||value.score<0||value.score>100||Number(value.questionsCorrect)>Number(value.questionsCompleted)||Number(value.questionsCompleted)>Number(value.attempts)||!Array.isArray(value.reviewQueue)||!value.reviewQueue.every(x=>typeof x==='string')){notice='Alguns registros inválidos não foram carregados. Os dados originais foram preservados.';continue;}
  // Não há avaliação implementada: um status salvo não comprova domínio.
  if(value.status==='completed')notice='Conclusões antigas não têm avaliação verificável. Foram mantidas como registros anteriores, sem liberar pré-requisitos.';
  state.progress[id]={moduleId:id,status:'in_progress',score:value.score,questionsCompleted:Number(value.questionsCompleted),questionsCorrect:Number(value.questionsCorrect),attempts:Number(value.attempts),hintsUsed:Number(value.hintsUsed),reviewQueue:[...value.reviewQueue] as string[],startedAt:date(value.startedAt),lastStudied:date(value.lastStudied)};
 }
 if(!legacy)state.savedModules=[...new Set((data.savedModules as unknown[]).filter((id):id is string=>typeof id==='string'&&ids.has(id)))];
 return {state,notice};
}
export function loadStudyState(storage:StoragePort,modules:readonly Module[]){
 try{const current=storage.getItem(STORAGE_KEY);if(current!==null)return parseStudyState(current,modules);
 const legacy=storage.getItem('saep_progress');return legacy===null?{state:emptyState(),notice:''}:parseStudyState(legacy,modules,true);
 }catch{return {state:emptyState(),notice:'Armazenamento local indisponível. Você pode explorar a trilha, mas suas escolhas não serão salvas.'};}
}
export function saveStudyState(storage:StoragePort,state:StudyState):string{
 try{const previous=storage.getItem(STORAGE_KEY);if(previous!==null&&storage.getItem(BACKUP_KEY)===null)storage.setItem(BACKUP_KEY,previous);storage.setItem(STORAGE_KEY,JSON.stringify(state));return '';}catch{return 'Não foi possível salvar neste navegador. Suas escolhas permanecem nesta sessão.';}
}
export function validateModuleGraph(modules:readonly Module[]):string[]{
 const errors:string[]=[],ids=new Set<string>(),orders=new Set<number>();
 for(const m of modules){if(ids.has(m.id))errors.push(`ID duplicado: ${m.id}`);if(orders.has(m.order))errors.push(`Ordem duplicada: ${m.order}`);ids.add(m.id);orders.add(m.order);}
 const visits=new Set<string>(),done=new Set<string>();
 function visit(m:Module){if(visits.has(m.id)){errors.push(`Ciclo de pré-requisitos: ${m.id}`);return;}if(done.has(m.id))return;visits.add(m.id);for(const id of m.prerequisites){const p=modules.find(x=>x.id===id);if(!p)errors.push(`Pré-requisito inexistente: ${m.id} → ${id}`);else{if(p.order>=m.order)errors.push(`Pré-requisito fora de ordem: ${m.id} → ${id}`);visit(p);}}visits.delete(m.id);done.add(m.id);}
 modules.forEach(visit);return errors;
}

export function canStartModule(id:string,completed:readonly string[],modules:readonly Module[]):boolean{
 const module=modules.find(m=>m.id===id);return Boolean(module&&module.contentStatus==='ready'&&module.prerequisites.every(p=>completed.includes(p)));
}
