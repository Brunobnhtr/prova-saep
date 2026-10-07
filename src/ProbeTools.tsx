import {useRef,useState,useLayoutEffect,useEffect} from 'react';
import type {PointerEvent} from 'react';
type Color='red'|'black';
type Point={x:number,y:number};
type Drag={color:Color,point:Point,target:number|null};
export function ProbeTools({red,black,onConnect,onContact}:{red:number|null,black:number|null,onConnect:(color:Color,terminal:number|null)=>void,onContact:(touching:boolean)=>void}){
 const container=useRef<HTMLDivElement>(null);
 const [size,setSize]=useState({width:500,height:350});
 const [points,setPoints]=useState<Record<Color,Point>>({red:{x:300,y:270},black:{x:400,y:270}});
 const [drag,setDrag]=useState<Drag|null>(null);
 const current=useRef<Drag|null>(null);
 const pointerId=useRef<number|null>(null);
 const loose=useRef<Partial<Record<Color,Point>>>({});
 useLayoutEffect(()=>{
  const host=container.current?.parentElement;if(!host)return;
  const update=()=>{const rect=host.getBoundingClientRect();setSize({width:rect.width,height:rect.height});
   const locate=(color:Color,n:number|null):Point=>{const term=n===null?null:host.querySelector(`[data-terminal="${n}"]`)?.getBoundingClientRect();return term?{x:term.left-rect.left+term.width/2,y:term.top-rect.top+12}:loose.current[color]??{x:rect.width*(color==='red'?.7:.88),y:rect.height-75};};
   setPoints({red:locate('red',red),black:locate('black',black)});
  };update();const observer=new ResizeObserver(update);observer.observe(host);return ()=>observer.disconnect();
 },[red,black]);
 function position(e:PointerEvent):Drag{
  const host=container.current!.parentElement!;const rect=host.getBoundingClientRect();
  const point={x:Math.max(24,Math.min(rect.width-24,e.clientX-rect.left)),y:Math.max(24,Math.min(rect.height-62,e.clientY-rect.top))};
  let target:number|null=null;
  for(const el of host.querySelectorAll<HTMLElement>('[data-terminal]')){const box=el.getBoundingClientRect();if(e.clientX>=box.left-12&&e.clientX<=box.right+12&&e.clientY>=box.top-12&&e.clientY<=box.bottom+12)target=Number(el.dataset.terminal);}
  return {color:current.current!.color,point,target};
 }
 function start(e:PointerEvent<HTMLButtonElement>,color:Color){if(pointerId.current!==null)return;e.preventDefault();pointerId.current=e.pointerId;e.currentTarget.setPointerCapture(e.pointerId);current.current={color,point:points[color],target:null};setDrag(current.current);}
 function move(e:PointerEvent<HTMLButtonElement>){if(!current.current||pointerId.current!==e.pointerId)return;current.current=position(e);setDrag(current.current);}
 function finish(e:PointerEvent<HTMLButtonElement>,cancel=false){if(!current.current||pointerId.current!==e.pointerId)return;const dropped=cancel?current.current:position(e);if(!cancel){loose.current[dropped.color]=dropped.point;setPoints(p=>({...p,[dropped.color]:dropped.point}));onConnect(dropped.color,dropped.target);}current.current=null;pointerId.current=null;setDrag(null);if(e.currentTarget.hasPointerCapture(e.pointerId))e.currentTarget.releasePointerCapture(e.pointerId);}
 const display=(color:Color)=>drag?.color===color?drag.point:points[color];
 const r=display('red'),b=display('black');
 const touching=Math.hypot(r.x-b.x,r.y-b.y)<=28 && red===null && black===null;
 useEffect(()=>{onContact(touching);},[touching]);
 return <div ref={container} className="probe-tools">
  <svg width="100%" height="100%" aria-hidden="true">{(['red','black'] as const).map(color=>{const p=display(color),sx=size.width*(color==='red'?.42:.53);return <path key={color} d={`M ${sx} ${size.height-3} C ${sx-85} ${size.height+5}, ${p.x+65} ${p.y+125}, ${p.x} ${p.y+57}`} fill="none" stroke={color==='red'?'#b9322e':'#1c292d'} strokeWidth="6" strokeLinecap="round"/>;})}</svg>
  {(['red','black'] as const).map(color=>{const p=display(color);return <button key={color} type="button" className={`draggable-probe ${color} ${drag?.color===color?'held':''}`} style={{transform:`translate(${p.x-22}px,${p.y-8}px)`}} aria-label={`Arrastar ponta ${color==='red'?'vermelha':'preta'}`} onPointerDown={e=>start(e,color)} onPointerMove={move} onPointerUp={e=>finish(e)} onPointerCancel={e=>finish(e,true)} onKeyDown={e=>{if(e.key==='Delete'||e.key==='Backspace'){loose.current[color]=undefined;onConnect(color,null);}}}><span className="probe-tip"/><span className="probe-grip"/><span className="probe-label">{color==='red'?'V':'P'}</span></button>;})}
  {touching&&<span className="contact-mark">● PONTAS EM CONTATO</span>}
  {drag&&<div className="drag-tip">{touching?'Contato entre as pontas de prova':drag.target?'Solte no borne destacado':'Encoste na outra ponta para testar · ou em um borne para medir'}</div>}
 </div>;
}
