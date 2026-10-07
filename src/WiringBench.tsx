import {useState,useRef,useLayoutEffect,useEffect} from 'react';
import type {PointerEvent} from 'react';
import {evaluateWiring,type Wire} from './domain/wiring';
import {MotorScene,terminalNames,terminalLayout} from './MotorScene';
import {MotorNameplate} from './MotorNameplate';

type PairRecord={key:string,labels:number[],terminals:number[]};
type Point={x:number,y:number};
const external:Record<string,[number,number]>={L1:[145,70],L2:[270,70],L3:[395,70],PE:[540,70],J1:[65,235],J2:[65,305],J3:[65,375],J4:[65,445],CASE:[555,520]};
function PlateDialog({onClose}:{onClose:()=>void}){
 const ref=useRef<HTMLDialogElement>(null);
 useEffect(()=>{ref.current?.showModal();return()=>ref.current?.close();},[]);
 return <dialog ref={ref} className="plate-dialog" onCancel={onClose} onClick={e=>{if(e.target===e.currentTarget)onClose();}}><button autoFocus onClick={onClose}>Fechar placa</button><MotorNameplate/></dialog>;
}
export function WiringBench({pairs,onReturn}:{pairs:PairRecord[],onReturn:()=>void}){
 const [wires,setWires]=useState<Wire[]>([]),[selected,setSelected]=useState<string|null>(null),[voltage,setVoltage]=useState(380),[running,setRunning]=useState(false),[feedback,setFeedback]=useState('Rede virtual isolada. Posicione os cabos e monte as conexões na caixa de bornes.');
 const [tool,setTool]=useState<'wire'|'bridge'>('wire'),[bridges,setBridges]=useState<string[]>([]),[plateOpen,setPlateOpen]=useState(false);
 const [placement,setPlacement]=useState<Record<number,number>>({1:1,2:2,3:3,4:4,5:5,6:6});
 const [points,setPoints]=useState<Record<string,Point>>({}),[ghost,setGhost]=useState<{id:string,x:number,y:number}|null>(null);
 const host=useRef<HTMLDivElement>(null),skipClick=useRef(false),drag=useRef<{id:string,pointer:number}|null>(null);
 const key=(a:string,b:string)=>[a,b].sort().join('-');
 const cableNumber=(n:number)=>{const p=pairs.find(p=>p.terminals.includes(n));return p?.labels[p.terminals.indexOf(n)]??'?';};
 const label=(id:string)=>id==='CASE'?'Carcaça':id.startsWith('M')?`Cabo ${cableNumber(Number(id.slice(1)))}`:id;
 useLayoutEffect(()=>{
  const element=host.current;if(!element)return;
  const update=()=>{const bounds=element.getBoundingClientRect(),next:Record<string,Point>={};
   for(const button of element.querySelectorAll<HTMLElement>('[data-port]')){const box=(button.querySelector('.bolt,i')??button).getBoundingClientRect();next[button.dataset.port!]={x:(box.left+box.width/2-bounds.left)*640/bounds.width,y:box.top+box.height/2-bounds.top};}
   setPoints(next);
  };update();const observer=new ResizeObserver(update);observer.observe(element);return()=>observer.disconnect();
 },[placement]);
 function link(a:string,b:string){
  if(running||a===b)return;
  if(tool==='bridge'&&(!a.startsWith('M')||!b.startsWith('M'))){setFeedback('As pontes ficam entre os bornes do motor. Selecione cabo para rede, PE ou conector.');setSelected(null);return;}
  if(!wires.some(w=>w.includes(a)&&w.includes(b))){setWires(w=>[...w,[a,b]]);if(tool==='bridge')setBridges(p=>[...p,key(a,b)]);}
  setSelected(null);setFeedback('Conexão montada na bancada. Rede virtual continua isolada.');
 }
 function select(id:string){if(running)return;if(selected===id)setSelected(null);else if(selected)link(selected,id);else setSelected(id);}
 function down(e:PointerEvent<HTMLButtonElement>,id:string){if(running||drag.current)return;drag.current={id,pointer:e.pointerId};e.currentTarget.setPointerCapture(e.pointerId);}
 function move(e:PointerEvent<HTMLButtonElement>){if(!drag.current||drag.current.pointer!==e.pointerId)return;const box=host.current!.getBoundingClientRect();setGhost({id:drag.current.id,x:(e.clientX-box.left)*640/box.width,y:Math.max(0,Math.min(580,e.clientY-box.top))});}
 function release(e:PointerEvent<HTMLButtonElement>,cancel=false){
  if(!drag.current||drag.current.pointer!==e.pointerId)return;const source=drag.current.id;
  const target=cancel?null:document.elementFromPoint(e.clientX,e.clientY)?.closest<HTMLElement>('[data-port]')?.dataset.port;
  setGhost(null);drag.current=null;if(target&&target!==source){skipClick.current=true;link(source,target);}
  if(e.currentTarget.hasPointerCapture(e.pointerId))e.currentTarget.releasePointerCapture(e.pointerId);
 }
 const handlers=(id:string)=>({onClick:()=>{if(skipClick.current){skipClick.current=false;return;}select(id);},onPointerDown:(e:PointerEvent<HTMLButtonElement>)=>down(e,id),onPointerMove:move,onPointerUp:(e:PointerEvent<HTMLButtonElement>)=>release(e),onPointerCancel:(e:PointerEvent<HTMLButtonElement>)=>release(e,true)});
 function positionCable(slot:number,cable:number){if(running||wires.length)return;const other=Number(Object.keys(placement).find(k=>placement[Number(k)]===cable));setPlacement(p=>({...p,[slot]:cable,[other]:p[slot]}));setSelected(null);setFeedback('Posição alterada. As etiquetas continuam sendo as suas; a orientação ainda não está validada.');}
 function start(){const result=evaluateWiring(wires,voltage);setRunning(result.ok);setFeedback(result.message);setSelected(null);}
 function remove(index:number){const [a,b]=wires[index];setWires(w=>w.filter((_,i)=>i!==index));setBridges(p=>p.filter(k=>k!==key(a,b)));setFeedback('Conexão removida. Rede virtual isolada.');}
 return <section className="wiring-lab" aria-label="Fechamento do motor">
  <div className="wiring-head"><div><p className="eyebrow">02 / MESMO MOTOR · CAIXA DE BORNES</p><h2>Monte na própria caixa do motor.</h2></div><button onClick={onReturn} disabled={running}>Voltar à identificação</button></div>
  <div className="wiring-layout"><div>
   <div className="wire-toolbar"><span className={running?'live-lamp':'isolated-lamp'}>● {running?'EM FUNCIONAMENTO VIRTUAL':'REDE VIRTUAL ISOLADA'}</span><div className="wiring-tools"><button disabled={running} aria-pressed={tool==='wire'} onClick={()=>{setTool('wire');setSelected(null);}}>Cabo pelas canaletas</button><button disabled={running} aria-pressed={tool==='bridge'} onClick={()=>{setTool('bridge');setSelected(null);}}>Ponte entre bornes</button><button disabled={running||!selected} onClick={()=>setSelected(null)}>Cancelar</button></div></div>
   <p className="wiring-help">Amplie a placa no corpo do motor. Arraste ou clique nas duas portas para ligar. Pontes ficam na caixa de bornes; cabos passam pelas canaletas. J1–J4 são conectores de emenda, cruzamentos não conectam.</p>
   <div className="diagram-scroll"><div ref={host} className="connection-diagram motor-connection-scene">
    <svg preserveAspectRatio="none" viewBox="0 0 640 580" aria-hidden="true"><rect className="duct" x="25" y="135" width="590" height="45" rx="5"/><rect className="duct" x="25" y="490" width="590" height="45" rx="5"/>
     {wires.map(([a,b],i)=>{const p=points[a],q=points[b];if(!p||!q)return null;const bridge=bridges.includes(key(a,b)),lane=(a==='CASE'||b==='CASE'?498:144)+(i%6)*5;
      return <path key={key(a,b)} className={bridge?'wire terminal-bridge':running?'wire energized':'wire'} stroke={bridge?'#d8af62':a==='PE'||b==='PE'||a==='CASE'||b==='CASE'?'#8dc652':['#e1a24b','#80cbd5','#c58ceb'][i%3]} d={bridge?`M${p.x} ${p.y} L${q.x} ${q.y}`:`M${p.x} ${p.y} V${lane} H${q.x} V${q.y}`}/>;})}
     {ghost&&points[ghost.id]&&<path className="wire ghost-wire" stroke="#fff" d={`M${points[ghost.id].x} ${points[ghost.id].y} L${ghost.x} ${ghost.y}`}/>}
    </svg>
    <span className="diagram-caption source-caption">REDE TRIFÁSICA · TENSÃO ENTRE FASES</span>
    <span className="diagram-caption motor-caption">MOTOR · SUAS ETIQUETAS NOS CABOS</span>
    <MotorScene running={running} onPlate={()=>setPlateOpen(true)} terminal={slot=>{const id=`M${placement[slot]}`;return <button key={slot} data-port={id} disabled={running} aria-label={`Conectar ${label(id)}`} aria-pressed={selected===id} className="motor-wire-port" {...handlers(id)}><span className="motor-lead"/><span className="bolt"/><b className="winding-label">{cableNumber(placement[slot])}</b><span className="socket-label">Posição {terminalNames[slot]}</span></button>;}}/>
    {Object.entries(external).map(([id,[x,y]])=><button key={id} className="external-port" data-port={id} disabled={running} aria-label={`Conectar ${label(id)}`} aria-pressed={selected===id} style={{left:`${x/640*100}%`,top:y}} {...handlers(id)}><i/>{label(id)}</button>)}
   </div></div>
   <div className="wire-list">{wires.map(([a,b],i)=><button disabled={running} key={key(a,b)} onClick={()=>remove(i)}>{bridges.includes(key(a,b))?'Ponte: ':''}{label(a)} → {label(b)} <span>×</span></button>)}{!wires.length&&<span>Nenhum cabo ou ponte montado.</span>}</div>
   <details className="cable-placement"><summary>Posicionar os cabos nos bornes de referência</summary><p>As posições U1…W2 são referências da placa. Sua etiqueta numérica não identifica automaticamente início/fim. Posicione antes de montar; remova as conexões para reposicionar.</p><div>{terminalLayout.map(slot=><label key={slot}>Posição {terminalNames[slot]}<select aria-label={`Cabo na posição ${terminalNames[slot]}`} disabled={running||wires.length>0} value={placement[slot]} onChange={e=>positionCable(slot,Number(e.target.value))}>{[1,2,3,4,5,6].map(n=><option key={n} value={n}>Cabo {cableNumber(n)}</option>)}</select></label>)}</div></details>
  </div><aside className="wiring-controls">
   <MotorNameplate/><button className="enlarge-plate" onClick={()=>setPlateOpen(true)}>Ampliar placa e diagramas</button>
   <label>Tensão entre fases da fábrica<select disabled={running} value={voltage} onChange={e=>{setVoltage(Number(e.target.value));setFeedback('Tensão de entrada alterada. Confira a placa antes da partida.');}}><option value="220">220 V</option><option value="380">380 V</option></select></label>
   <div className={`rotor ${running?'spinning':''}`} aria-label={running?'Eixo girando':'Eixo parado'}><span/></div>
   <button className="start-motor" disabled={running} onClick={start}>Solicitar partida virtual</button><button className="stop-motor" onClick={()=>{setRunning(false);setFeedback('Motor parado. Rede virtual isolada; edição liberada.');}}>Parar e isolar</button>
   <p role="status" aria-live="polite">{feedback}</p><small>Partida direta virtual com fechamento escolhido pela placa. Modelo ideal sem carga; não calcula correntes ou proteções reais. Não é partida automática estrela-triângulo.</small>
  </aside></div>{plateOpen&&<PlateDialog onClose={()=>setPlateOpen(false)}/>}
 </section>;
}
