import {useEffect,useRef} from 'react';
/** Sinal sonoro didático contínuo enquanto o contato permanecer fechado. */
export function useContinuityTone(active:boolean,enabled:boolean,onError:()=>void){
 const audio=useRef<AudioContext|null>(null);
 useEffect(()=>{
  if(!active||!enabled)return;
  let oscillator:OscillatorNode|undefined,gain:GainNode|undefined,cancelled=false;
  try{
   const ctx=audio.current??=new AudioContext();
   void ctx.resume().then(()=>{
    if(cancelled)return;
    oscillator=ctx.createOscillator();gain=ctx.createGain();
    oscillator.frequency.value=780;gain.gain.value=.035;
    oscillator.connect(gain);gain.connect(ctx.destination);oscillator.start();
   }).catch(onError);
  }catch{onError();}
  return ()=>{cancelled=true;oscillator?.stop();oscillator?.disconnect();gain?.disconnect();};
 },[active,enabled]);
 useEffect(()=>()=>{void audio.current?.close();},[]);
}
