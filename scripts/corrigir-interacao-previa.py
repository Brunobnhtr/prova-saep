from pathlib import Path
p=Path('src/main.tsx');s=p.read_text(encoding='utf-8')
s=s.replace("useState,useRef,useEffect","useState,useRef,useEffect,useLayoutEffect")
s=s.replace("function App(){",'''function ProbeWires({red,black}:{red:number|null,black:number|null}){
 const svg=useRef<SVGSVGElement|null>(null);const [paths,setPaths]=useState<{color:string,d:string}[]>([]);
 useLayoutEffect(()=>{
  const host=svg.current?.parentElement;if(!host)return;
  const update=()=>{const box=host.getBoundingClientRect();setPaths(([['#bb302b',red,0],['#202a30',black,1]] as const).map(([color,n,index])=>{
   const terminal=n===null?null:host.querySelector(`[data-terminal="${n}"]`)?.getBoundingClientRect();
   const x=terminal?terminal.left-box.left+terminal.width/2:box.width*(index===0?.72:.88),y=terminal?terminal.top-box.top+12:box.height-45;
   const startX=box.width*(index===0?.44:.57),startY=box.height-4;
   return {color,d:`M ${startX} ${startY} C ${startX-90} ${startY-15}, ${x+65} ${y+125}, ${x} ${y+30} L ${x} ${y}`};
  }));};update();const observer=new ResizeObserver(update);observer.observe(host);return ()=>observer.disconnect();
 },[red,black]);
 return <svg ref={svg} className="probe-wires" aria-label="Cordões de teste vermelho e preto até os terminais selecionados" role="img">{paths.map(p=><g key={p.color}><path d={p.d} stroke="#eef1e6" strokeWidth="9"/><path d={p.d} stroke={p.color} strokeWidth="5"/></g>)}</svg>;
}
function App(){''')
s=s.replace("function select(n:number){if(!ready)return;", "function select(n:number){if(!ready){setNote(instruction);return;}")
s=s.replace("if(measure(a,b,true)==='closed')beep();}","setNote(`${probe==='red'?'Ponta vermelha':'Ponta preta'} conectada ao terminal ${n}. ${a===null||b===null?'Conecte a outra ponta para medir.':measure(a,b,true)==='closed'?'Continuidade detectada.':'Sem continuidade entre os terminais.'}`);if(measure(a,b,true)==='closed')beep();}")
s=s.replace(" function beep()", " const instruction=!safe?`Passo ${stage+1}: confirme ${preparation[stage].toLowerCase()} abaixo.`:mode!=='continuity'?'Selecione Ω / ))) no multímetro.':!tested?'Clique em Unir pontas e testar instrumento.':`Medição liberada: selecione um terminal para a ponta ${probe==='red'?'vermelha':'preta'}.`;\n function beep()")
s=s.replace('<div className="workspace">', '''<section className="guide" aria-label="Próxima ação"><strong>{instruction}</strong><div className="quick-preparation">{preparation.map((step,i)=><button key={step} disabled={i!==stage} onClick={()=>{setStage(i+1);setNote('');}}>{i<stage?'✓':i+1} · {step}</button>)}</div><p role="status" aria-live="polite">{note}</p></section><div className="workspace">''')
s=s.replace('key={n} disabled={!ready}', 'key={n} data-terminal={n} aria-disabled={!ready}')
s=s.replace('<span className="bolt"/>','<span className="motor-lead"/><span className="bolt"/>')
s=s.replace('</div></div></div><div className="probes">','</div></div><ProbeWires red={red} black={black}/></div><div className="probes">')
s=s.replace("onClick={()=>setProbe('red')}","onClick={()=>{setProbe('red');setNote(ready?'Ponta vermelha selecionada. Clique no terminal que deseja medir.':instruction);}}")
s=s.replace("onClick={()=>setProbe('black')}","onClick={()=>{setProbe('black');setNote(ready?'Ponta preta selecionada. Clique no terminal que deseja medir.':instruction);}}")
# Mantém as mesmas confirmações acessíveis em um único lugar, acima da bancada.
start=s.index('<ol>{preparation.map')
end=s.index('</ol>',start)+len('</ol>')
s=s[:start]+'<p>{safe?"✓ Cenário preparado. Termine o teste do instrumento para medir.":"Conclua os passos indicados acima da bancada."}</p>'+s[end:]
p.write_text(s,encoding='utf-8')
css=Path('src/style.css');css.write_text(css.read_text(encoding='utf-8')+'''
.guide{background:#fff;border-left:5px solid #de782e;padding:18px;margin-bottom:20px}.guide strong{display:block;line-height:1.6}.guide p{margin:10px 0 0;font-size:14px;min-height:20px}.quick-preparation{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.quick-preparation button{flex:1 1 210px;min-height:48px;text-align:left;padding:10px;border:1px solid #7c9586;background:#e2eade;color:#1f3932}.probe-wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;overflow:visible}.probe-wires path{fill:none;stroke-linecap:round;stroke-linejoin:round}.motor-lead{position:absolute;top:100%;left:50%;height:32px;width:6px;background:linear-gradient(90deg,#5b4831,#c49d62,#5b4831);border-radius:0 0 4px 4px;pointer-events:none}.terminals button[aria-disabled=true]{filter:grayscale(.7);opacity:.7}.terminals button{margin-bottom:12px}.terminalbox{padding-bottom:34px}.terminals{gap:14px}.motor{height:350px}.probes button{min-height:48px}@media(max-width:760px){.motor{height:325px}.quick-preparation button{flex-basis:100%}.terminalbox{padding-bottom:30px}}
''',encoding='utf-8')
