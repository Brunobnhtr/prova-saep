import {useState} from 'react';
import type {Module} from '../types';
import {isModuleUnlocked} from '../data/modules';
interface Props{modules:Module[];completedModules:string[];savedModules:string[];onSelectModule:(module:Module)=>void}
const normalize=(value:string)=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function ModuleCatalog({modules,completedModules,savedModules,onSelectModule}:Props){
 const [query,setQuery]=useState(''),[area,setArea]=useState('Todas'),[filter,setFilter]=useState('all');
 const areas=[...new Set(modules.map(m=>m.area))];
 const visible=modules.filter(m=>(area==='Todas'||m.area===area)&&normalize(`${m.code} ${m.subtitle} ${m.area} ${m.theme}`).includes(normalize(query))&&(filter==='all'||filter==='saved'&&savedModules.includes(m.id)||filter==='initial'&&m.prerequisites.length===0));
 return <section id="catalog" className="module-catalog"><div className="catalog-heading"><div><p className="eyebrow">35 TEMAS / UMA BASE DE CADA VEZ</p><h2>Sua trilha de estudo</h2><p>A ordem orienta o estudo; os pré-requisitos indicam o que aprender antes.</p></div><span className="catalog-count">{visible.length} de {modules.length} temas</span></div>
 <div className="catalog-filters"><label className="search-label">Buscar um tema<input type="search" placeholder="Ex.: segurança, multímetro, motores…" value={query} onChange={e=>setQuery(e.target.value)}/></label><label>Área<select aria-label="Área" value={area} onChange={e=>setArea(e.target.value)}><option>Todas</option>{areas.map(a=><option key={a}>{a}</option>)}</select></label><label>Mostrar<select aria-label="Mostrar" value={filter} onChange={e=>setFilter(e.target.value)}><option value="all">Toda a trilha</option><option value="initial">Sem pré-requisitos</option><option value="saved">Salvos para estudar</option></select></label></div>
 <p className="catalog-explanation">Você pode consultar todos os planos. Os conteúdos estão em preparação; pré-requisitos atendidos não significam aula publicada.</p>
 <div className="modules-grid">{visible.map(module=>{const unlocked=isModuleUnlocked(module.id,completedModules);return <button key={module.id} className={`module-card ${unlocked?'module-initial':''}`} onClick={()=>onSelectModule(module)} aria-label={`Ver plano ${module.code}: ${module.subtitle}`}><div className="card-top"><span className="module-order">{module.order.toString().padStart(2,'0')}</span><span className="content-badge">{module.contentStatus==='ready'?'Conteúdo publicado':module.contentStatus==='preview'?'Prévia':'Em preparação'}</span></div><span className="module-area">{module.area}</span><h3><span>{module.code}</span>{module.subtitle}</h3><p className="card-prerequisites">{unlocked?'Sem pré-requisitos pendentes':`Antes: ${module.prerequisites.join(' · ')}`}</p><div className="card-bottom"><span>{module.targetQuestions} questões planejadas</span><span>{savedModules.includes(module.id)?'Salvo · ':''}Ver plano ↗</span></div></button>;})}</div>
 {!visible.length&&<div className="empty-state"><h3>Nenhum tema nesta seleção.</h3><p>Tente outra busca ou explore todas as áreas.</p><button className="btn-secondary" onClick={()=>{setQuery('');setArea('Todas');setFilter('all');}}>Limpar filtros</button></div>}
 </section>;
}
export default ModuleCatalog;
