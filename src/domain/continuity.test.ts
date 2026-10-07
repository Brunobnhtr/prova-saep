import {expect,test} from 'vitest';
import {connected,measure,windings} from './continuity';
test('três bobinas e quinze combinações',()=>{let matches=0;for(let a=1;a<=6;a++)for(let b=a+1;b<=6;b++){const expected=(a===1&&b===5)||(a===2&&b===6)||(a===3&&b===4);expect(connected(a,b)).toBe(expected);if(connected(a,b))matches++;}expect(matches).toBe(3);});
test('equivalência e caminho indireto',()=>{expect(connected(5,1,[...windings].reverse())).toBe(true);expect(connected(1,6,[[1,2],[2,6]])).toBe(true);expect(connected(1,6,[])).toBe(false);});
test('interação bloqueada antes do preparo e pontas incompletas',()=>{expect(measure(1,5,false)).toBe('blocked');expect(measure(null,5,true)).toBe('waiting');expect(measure(1,5,true)).toBe('closed');expect(measure(1,2,true)).toBe('open');});
