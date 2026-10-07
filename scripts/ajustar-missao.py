from pathlib import Path
p=Path('src/main.tsx');s=p.read_text(encoding='utf-8')
s=s.replace(' const audio=',' const [resetId,setResetId]=useState(0);\n const audio=')
s=s.replace('key={`${stage===0&&!tested&&red===null&&black===null}`}','key={resetId}')
s=s.replace('function reset(){setStage','function reset(){setResetId(id=>id+1);setStage')
s=s.replace("setPairs(p=>p.includes(key)?p:[...p,key]);", "if(pairs.includes(key)){setNote('Esse par já foi registrado. Procure outra bobina.');return;}setPairs(p=>[...p,key]);setNote(`Bobina encontrada: ${key}. ${pairs.length===2?'Missão concluída!':'Procure o próximo par.'}`);")
s=s.replace('<div className="workspace">','<div className="mission"><div><b>MISSÃO · Identificar 3 bobinas</b><span>Arraste, meça e registre cada par. Sem pontes entre os bornes.</span></div><progress max="3" value={pairs.length} aria-label="Bobinas identificadas"/><strong>{pairs.length}/3</strong></div><div className="workspace">')
p.write_text(s,encoding='utf-8')
css=Path('src/style.css');css.write_text(css.read_text(encoding='utf-8')+'\n.mission{display:flex;align-items:center;gap:18px;background:#203f37;color:#fff;padding:18px;margin-bottom:18px}.mission div{flex:1}.mission b{display:block;font-size:14px}.mission span{display:block;font-size:12px;margin-top:7px;color:#d3e0d6}.mission progress{width:110px;accent-color:#e7a93b}.mission strong{font-size:20px}@media(max-width:760px){.mission{flex-wrap:wrap}.mission div{flex-basis:100%}}\n',encoding='utf-8')
