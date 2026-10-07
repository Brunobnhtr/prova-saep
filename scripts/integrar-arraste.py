from pathlib import Path
p=Path('src/main.tsx');s=p.read_text(encoding='utf-8')
start=s.index('function ProbeWires');end=s.index('function App(){');s=s[:start]+s[end:]
s=s.replace('useEffect,useLayoutEffect','useEffect')
s=s.replace("import './style.css';","import './style.css';\nimport {ProbeTools} from './ProbeTools';")
s=s.replace('function save(){',"""function connect(color:'red'|'black',n:number|null){const a=color==='red'?n:red,b=color==='black'?n:black;if(color==='red')setRed(n);else setBlack(n);setProbe(color==='red'?'black':'red');setNote(n===null?'Ponta desconectada.':!ready?`Ponta encaixada no terminal ${n}. Medição bloqueada: ${instruction}`:`Ponta encaixada no terminal ${n}. ${measure(a,b,true)==='closed'?'Continuidade detectada.':'Verifique a leitura do instrumento.'}`);if(measure(a,b,ready)==='closed')beep();}
 function save(){""")
s=s.replace('<ProbeWires red={red} black={black}/>','<ProbeTools key={`${stage===0&&!tested&&red===null&&black===null}`} red={red} black={black} onConnect={connect}/>')
s=s.replace('Medição liberada: selecione um terminal para a ponta','Medição liberada: arraste as pontas até os bornes. Alternativa por clique: ponta')
s=s.replace('Selecione a ponta e depois um terminal. Toque ou use Tab e Enter.','Pegue a ponta vermelha ou preta e arraste até o borne. Para teclado, selecione a ponta abaixo e depois o terminal.')
p.write_text(s,encoding='utf-8')
css=Path('src/style.css');css.write_text(css.read_text(encoding='utf-8')+'''
.probe-tools{position:absolute;inset:0;z-index:6;pointer-events:none}.probe-tools svg{position:absolute;inset:0;overflow:visible}.draggable-probe{position:absolute;left:0;top:0;width:44px;height:75px;padding:0;border:0;background:none;pointer-events:auto;touch-action:none;cursor:grab;user-select:none;z-index:3}.draggable-probe.held{cursor:grabbing;filter:drop-shadow(0 6px 4px #0005)}.probe-tip{position:absolute;top:0;left:20px;width:4px;height:22px;background:linear-gradient(90deg,#eee,#718589);border-radius:4px 4px 0 0}.probe-grip{position:absolute;top:20px;left:13px;width:18px;height:48px;border-radius:7px;background:linear-gradient(90deg,#69201c,#e25243,#8c2924);box-shadow:inset 0 0 0 2px #ffffff30}.draggable-probe.black .probe-grip{background:linear-gradient(90deg,#111a1d,#546467,#1b282d)}.probe-label{position:absolute;top:36px;left:17px;color:white;font-size:12px;font-weight:bold}.drag-tip{position:absolute;bottom:2px;left:0;right:0;background:#163e37;color:white;padding:6px 10px;font-size:12px;z-index:5}.terminals button{transition:background-color .15s}.terminals .red,.terminals .black{background:#dfc588}.draggable-probe:focus-visible{outline:3px solid #ed8c39;outline-offset:0;border-radius:8px}
''',encoding='utf-8')
