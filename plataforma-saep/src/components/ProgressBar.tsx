interface Props{completed:number;total:number;percentage:number}
function ProgressBar({completed,total,percentage}:Props){
 const value=Math.max(0,Math.min(100,Number.isFinite(percentage)?percentage:0));
 return <div className="progress-container"><div className="progress-info"><span>Progresso de aprendizagem</span><b>{completed} / {total}</b></div><progress max="100" value={value} aria-label="Progresso de aprendizagem"/><span className="progress-caption">{value}% · conclusões verificadas</span></div>;
}
export default ProgressBar;
