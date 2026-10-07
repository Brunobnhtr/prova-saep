import {windings} from './continuity';
export type Wire=readonly [string,string];
export function evaluateWiring(wires:readonly Wire[],voltage:number){
 const parent=new Map<string,string>();
 function root(n:string):string{const p=parent.get(n);if(!p)return n;const r=root(p);parent.set(n,r);return r;}
 for(const [a,b] of wires){const x=root(a),y=root(b);if(x!==y)parent.set(x,y);}
 const phases=['L1','L2','L3'].map(root),pe=root('PE');
 if(new Set(phases).size!==3)return {ok:false,message:'Proteção atuou: fases unidas diretamente.'};
 if(phases.includes(pe)||phases.includes(root('CASE')))return {ok:false,message:'Proteção atuou: fase conectada ao circuito de proteção ou à carcaça.'};
 if(root('CASE')!==pe)return {ok:false,message:'Partida bloqueada: falta conectar PE à carcaça.'};
 const groups=[1,2,3,4,5,6].map(n=>root(`M${n}`));
 if(groups.includes(pe))return {ok:false,message:'Proteção atuou: cabo de enrolamento conectado ao PE.'};
 const unique=[...new Set(groups)],floating=unique.filter(n=>!phases.includes(n));
 const star=unique.length===4&&floating.length===1&&groups.filter(n=>n===floating[0]).length===3&&phases.every(p=>groups.filter(n=>n===p).length===1);
 const delta=unique.length===3&&floating.length===0&&phases.every(p=>groups.filter(n=>n===p).length===2);
 if(!star&&!delta)return {ok:false,message:'Partida bloqueada: fechamento incompleto ou topologia incompatível.'};
 const vectors=phases.map((_,i)=>({x:Math.cos(i*2*Math.PI/3),y:Math.sin(i*2*Math.PI/3)}));
 const potential=(n:string)=>vectors[phases.indexOf(n)]??{x:0,y:0};
 const coils=windings.map(([a,b])=>{const x=potential(root(`M${a}`)),y=potential(root(`M${b}`));return {x:x.x-y.x,y:x.y-y.y};});
 const magnitude=star?1:Math.sqrt(3);
 if(coils.some(v=>Math.abs(Math.hypot(v.x,v.y)-magnitude)>.001)||Math.hypot(coils.reduce((s,v)=>s+v.x,0),coils.reduce((s,v)=>s+v.y,0))>.001)return {ok:false,message:'Proteção didática: orientação dos enrolamentos incompatível. Revise as etiquetas e o fechamento.'};
 const connection=star?'estrela':'triângulo';
 if((star&&voltage!==380)||(delta&&voltage!==220))return {ok:false,message:`Ligação ${connection} incompatível com a rede de ${voltage} V e a placa Δ 220 / Y 380 V.`};
 return {ok:true,message:`Motor em funcionamento virtual · ${connection} · ${voltage} V. Modelo ideal sem carga.`};
}
