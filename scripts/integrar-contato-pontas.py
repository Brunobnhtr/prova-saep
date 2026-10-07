from pathlib import Path
p=Path('src/main.tsx');s=p.read_text(encoding='utf-8')
s=s.replace(' const audio=',' const [tipsTouch,setTipsTouch]=useState(false);\n const audio=')
s=s.replace("const result=measure(red,black,ready);","const result=safe&&mode==='continuity'&&tipsTouch?'closed':measure(red,black,ready);")
s=s.replace("'Clique em Unir pontas e testar instrumento.'","'Arraste a parte metálica de uma ponta até a outra para testar o instrumento.'")
s=s.replace(' function select(n:number)',""" useEffect(()=>{if(!tipsTouch)return;if(!safe){setNote('Pontas em contato. Conclua o preparo da bancada antes de testar o instrumento.');return;}if(mode!=='continuity'){setNote('Pontas em contato. Selecione Ω / ))) para testar continuidade.');return;}setTested(true);setNote('Pontas em contato: continuidade detectada. Instrumento testado. Separe as pontas e meça os bornes.');beep();},[tipsTouch,safe,mode]);
 function select(n:number)""")
s=s.replace('onConnect={connect}/>','onConnect={connect} onContact={setTipsTouch}/>')
s=s.replace("function reset(){setResetId", "function reset(){setTipsTouch(false);setResetId")
s=s.replace("{!ready?'— —':result==='waiting'?'— —':result==='closed'?'BAIXA R':'OL'}", "{result==='closed'?'BAIXA R':!ready?'— —':result==='waiting'?'OL':'OL'}")
s=s.replace("{result==='closed'?'● Caminho fechado · [bip curto]'", "{result==='closed'?(tipsTouch?'● Pontas em contato · [bip curto]':'● Caminho fechado · [bip curto]')")
p.write_text(s,encoding='utf-8')
css=Path('src/style.css');css.write_text(css.read_text(encoding='utf-8')+'\n.contact-mark{position:absolute;bottom:35px;left:8px;background:#c9e9b7;color:#193e29;border:1px solid #547b48;padding:7px 12px;font-size:12px;font-weight:bold}\n',encoding='utf-8')
