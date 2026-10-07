export type Pair = readonly [number,number];
export const windings: readonly Pair[] = [[1,5],[2,6],[3,4]];
export const preparation = ['Motor isolado da fonte do cenário','Reenergização impedida','Ausência de tensão constatada no cenário','Área e proteção verificadas no cenário'] as const;
// Cenário isolado de bancada. Esta lista não substitui o procedimento completo da NR-10.
export function connected(a:number,b:number,edges:readonly Pair[]=windings):boolean {
  const queue=[a],seen=new Set<number>();
  while(queue.length){const n=queue.shift()!;if(n===b)return true;if(seen.has(n))continue;seen.add(n);for(const [x,y] of edges){if(x===n)queue.push(y);if(y===n)queue.push(x);}}
  return false;
}
export function measure(a:number|null,b:number|null,ready:boolean):'blocked'|'waiting'|'closed'|'open'{
  if(!ready)return 'blocked';if(a===null||b===null)return 'waiting';return connected(a,b)?'closed':'open';
}
