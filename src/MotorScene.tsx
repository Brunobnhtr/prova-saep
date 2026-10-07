import type {ReactNode} from 'react';
export const terminalLayout=[4,5,6,1,2,3];
export const terminalNames:Record<number,string>={1:'U1',2:'V1',3:'W1',4:'W2',5:'U2',6:'V2'};
export function MotorScene({terminal,children,running=false,onPlate}:{terminal:(slot:number)=>ReactNode,children?:ReactNode,running?:boolean,onPlate?:()=>void}){
 return <div className={`motor ${running?'motor-running':''}`}><div className="motor-feet"/><div className="shaft"><span className={running?'shaft-spin':''}/></div><div className="housing"><div className="fins"/><div className="fan-cover"/>{onPlate?<button className="motorplate plate-trigger" onClick={onPlate}>MOTOR TRIFÁSICO<br/>Δ 220 / Y 380 V<br/><strong>AMPLIAR PLACA ↗</strong></button>:<span className="motorplate">MOTOR TRIFÁSICO<br/>Δ 220 / Y 380 V</span>}</div><div className="terminalbox"><div className="terminals">{terminalLayout.map(terminal)}</div></div>{children}</div>;
}
