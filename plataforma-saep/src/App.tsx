import {useState} from 'react';
import {MODULES} from './data/modules';
import {loadStudyState,saveStudyState,emptyState} from './domain/study';
import ModuleCatalog from './components/ModuleCatalog';
import ModuleDetail from './components/ModuleDetail';
import ProgressBar from './components/ProgressBar';
import './App.css';
function App(){
 const [loaded]=useState(()=>{try{return loadStudyState(window.localStorage,MODULES);}catch{return {state:emptyState(),notice:'Armazenamento local indisponível. As escolhas valem apenas nesta sessão.'};}});
 const [study,setStudy]=useState(loaded.state),[notice,setNotice]=useState(loaded.notice),[selectedId,setSelectedId]=useState<string|null>(null);
 const selected=MODULES.find(m=>m.id===selectedId);
 // A plataforma atual não possui avaliação para declarar módulos concluídos.
 const completed:string[]=[];
 const ready=MODULES.filter(m=>m.contentStatus==='ready').length;
 function toggleSaved(id:string){if(!MODULES.some(m=>m.id===id))return;
  const next={...study,savedModules:study.savedModules.includes(id)?study.savedModules.filter(x=>x!==id):[...study.savedModules,id]};setStudy(next);
  try{const error=saveStudyState(window.localStorage,next);if(error)setNotice(error);}catch{setNotice('Armazenamento indisponível. Suas escolhas permanecem nesta sessão.');}
 }
 function navigate(id:string|null){setSelectedId(id);window.scrollTo({top:0,behavior:'instant'});}
 return <div className="app"><a className="skip-link" href="#study-main">Ir para o conteúdo</a><header className="app-header"><a className="wordmark" href="#" onClick={e=>{e.preventDefault();navigate(null);}}>SAEP<span>caderno de eletrotécnica</span></a><div className="header-right"><span className="build-badge">PRÉVIA DA TRILHA</span><span>35 temas · estudo por etapas</span></div></header>
 <main id="study-main" className="app-main">{notice&&<div className="storage-notice" role="status">{notice}<button onClick={()=>setNotice('')} aria-label="Fechar aviso">×</button></div>}
 {selected?<ModuleDetail key={selected.id} module={selected} completedModules={completed} progress={study.progress[selected.id]} saved={study.savedModules.includes(selected.id)} onBack={()=>navigate(null)} onToggleSaved={()=>toggleSaved(selected.id)}/>:<>
 <section className="study-hero"><div><p className="eyebrow">SEU PLANO DE ESTUDO / ELETROTÉCNICA</p><h1>Entender primeiro.<br/><em>Praticar para aprender.</em></h1><p>Da segurança ao diagnóstico: uma trilha para conectar conceitos, instrumentos e decisões de bancada.</p><div className="hero-actions"><button className="btn-primary" onClick={()=>navigate('S01')}>Conhecer o primeiro tema <span>↗</span></button><a href="#catalog">Explorar a trilha ↓</a></div><span className="hero-note">Conteúdos em preparação. Nenhuma avaliação disponível nesta versão.</span></div><div className="hero-diagram" aria-hidden="true"><span>01 / OBSERVAR · 02 / MEDIR · 03 / DECIDIR</span><svg viewBox="0 0 440 220"><defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#ffffff18"/></pattern></defs><rect width="440" height="220" fill="url(#grid)"/><path d="M35 110 H105 V55 H250 V110 H390 M105 110 V170 H250 V110" fill="none" stroke="#d9ad67" strokeWidth="3"/><rect x="135" y="36" width="70" height="38" fill="#243e42" stroke="#d9ad67" strokeWidth="2"/><circle cx="170" cy="170" r="25" fill="#243e42" stroke="#abc4bd" strokeWidth="2"/><path d="M151 170 H189 M170 151 V189" stroke="#abc4bd"/><circle cx="315" cy="110" r="31" fill="#243e42" stroke="#d9ad67" strokeWidth="2"/><text x="315" y="119" textAnchor="middle" fill="#e2d7bf" fontFamily="monospace" fontSize="24">M</text>{[35,105,250,390].map(x=><circle key={x} cx={x} cy="110" r="5" fill="#d9ad67"/>)}</svg><div><b>O raciocínio vem antes da ligação.</b><p>Mapa de estudo · representação ilustrativa</p></div></div></section>
 <section className="overview" aria-label="Situação da plataforma"><ProgressBar completed={0} total={MODULES.length} percentage={0}/><div><b>{ready.toString().padStart(2,'0')}</b><span>temas com conteúdo publicado</span></div><div><b>{study.savedModules.length.toString().padStart(2,'0')}</b><span>temas salvos para estudar</span></div><div><b>35</b><span>temas planejados</span></div></section>
 <ModuleCatalog modules={MODULES} completedModules={completed} savedModules={study.savedModules} onSelectModule={m=>navigate(m.id)}/></>}
 </main><footer className="app-footer"><strong>SAEP / estudo pessoal</strong><p>Trilha editorial baseada no acervo analisado. Não é uma matriz oficial nem uma certificação do SENAI.</p><span>Conteúdo e avaliações serão publicados um módulo por vez.</span></footer></div>;
}
export default App;
