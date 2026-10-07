import {describe,it,expect} from 'vitest';
import {evaluateWiring,type Wire} from './wiring';
const pe:Wire=['PE','CASE'];
const star:Wire[]=[pe,['L1','M1'],['L2','M2'],['L3','M3'],['M5','J1'],['M6','J1'],['M4','J1']];
const delta:Wire[]=[pe,['L1','M1'],['L1','M4'],['L2','M2'],['L2','M5'],['L3','M3'],['L3','M6']];
describe('Montagem virtual por grafo',()=>{
 it('aceita estrela em 380 e triângulo em 220, incluindo conexões equivalentes',()=>{expect(evaluateWiring(star,380).ok).toBe(true);expect(evaluateWiring(delta,220).ok).toBe(true);expect(evaluateWiring(star.map(([a,b])=>[b,a]),380).ok).toBe(true);});
 it('recusa tensão incompatível, curto, ausência de PE, falta de fase e bobina invertida',()=>{for(const [w,v] of [[star,220],[delta,380],[star.slice(1),380],[star.slice(0,-1),380],[ [...star,['L1','L2']],380],[star.map(([a,b])=>[a,b==='M1'?'M5':b==='M5'?'M1':b]),380]] as [Wire[],number][])expect(evaluateWiring(w,v).ok).toBe(false);});
 it('não trata troca de duas fases como inversão de uma bobina',()=>{const swap=(n:string)=>n==='L1'?'L2':n==='L2'?'L1':n;expect(evaluateWiring(star.map(([a,b])=>[swap(a),swap(b)]),380).ok).toBe(true);});
});
