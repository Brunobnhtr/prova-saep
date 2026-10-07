function ConnectionDiagram({star}:{star:boolean}){
 const xs=[40,110,180],top=['W2','U2','V2'],bottom=['U1','V1','W1'];
 return <svg viewBox="0 0 220 152" role="img" aria-label={star?'Estrela: W2 U2 V2 unidos, fases em U1 V1 W1':'Triângulo: W2 com U1, U2 com V1, V2 com W1'}>
 {star?<path d="M40 38 H180" className="plate-bridge"/>:xs.map(x=><path key={x} d={`M${x} 38 V94`} className="plate-bridge"/>)}
 {xs.map((x,i)=><g key={x}><circle cx={x} cy="38" r="7"/><text x={x} y="20">{top[i]}</text><circle cx={x} cy="94" r="7"/><text x={x} y="78">{bottom[i]}</text><path d={`M${x} 102 V122`}/><text x={x} y="143">L{i+1}</text></g>)}
 </svg>;
}
export function MotorNameplate(){return <div className="nameplate detailed-nameplate"><div className="plate-title">MOTOR DE INDUÇÃO TRIFÁSICO<span>MODELO DIDÁTICO · 6 PONTAS</span></div><div className="plate-spec"><span>V<strong>220 / 380</strong></span><span>Hz<strong>60</strong></span><span>Ligação<strong>Δ / Y</strong></span></div><div className="plate-diagrams"><div><b>220 V · Δ TRIÂNGULO</b><ConnectionDiagram star={false}/></div><div><b>380 V · Y ESTRELA</b><ConnectionDiagram star/></div></div><p>Disposição de referência: W2–U2–V2 acima, U1–V1–W1 abaixo. As pontes só valem nessa disposição.</p><small>Placa didática baseada no arranjo de seis terminais da referência. Não reproduz uma ficha técnica WEG.</small></div>;}
