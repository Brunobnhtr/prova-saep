import {chromium} from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
const origin='http://127.0.0.1:5174';
try{
 for(const width of [1400,390]){
  console.log('Verificando interface',width);
  const context=await browser.newContext({viewport:{width,height:1000}}),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin);await page.getByRole('heading',{name:'Sua trilha de estudo'}).waitFor();
  if(await page.getByRole('button',{name:/^Ver plano /}).count()!==35)throw Error('Catálogo incompleto');
  await page.getByLabel('Buscar um tema').fill('seguranca');if(await page.getByRole('button',{name:/^Ver plano /}).count()!==3)throw Error('Busca sem acento');
  await page.getByLabel('Buscar um tema').fill('');await page.getByLabel('Mostrar',{exact:true}).selectOption('initial');if(await page.getByRole('button',{name:/^Ver plano /}).count()!==2)throw Error('Pré-requisitos iniciais');
  await page.getByRole('button',{name:/Ver plano S01:/}).click();await page.getByRole('heading',{name:'Este é o plano do tema.'}).waitFor();
  if(await page.getByRole('button',{name:/Iniciar módulo/}).count())throw Error('Conteúdo inexistente liberado');
  await page.getByRole('button',{name:'Salvar para estudar',exact:true}).click();await page.reload();await page.getByLabel('Mostrar',{exact:true}).selectOption('saved');
  if(await page.getByRole('button',{name:/^Ver plano /}).count()!==1)throw Error('Favorito não persistiu');
  await page.getByRole('button',{name:/Ver plano S01:/}).focus();await page.keyboard.press('Enter');await page.getByRole('button',{name:'✓ Salvo para estudar'}).waitFor();
  await page.getByRole('button',{name:'← Voltar à trilha'}).click();await page.getByRole('button',{name:/Ver plano S02:/}).click();await page.getByText('Pendente',{exact:true}).waitFor();await page.getByRole('button',{name:'← Voltar à trilha'}).click();
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Overflow');if(errors.length)throw Error(errors.join(';'));
  await page.screenshot({path:`output/previa/plataforma-revisada-${width}.png`,fullPage:true});await context.close();
 }
 for(const mode of ['corrupt','legacy','blocked','quota']){
  console.log('Verificando storage',mode);
  const context=await browser.newContext(),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(mode=>{
   if(mode==='blocked'){Object.defineProperty(window,'localStorage',{get(){throw Error('blocked')}});return;}
   if(mode==='quota'){Storage.prototype.setItem=function(){throw new DOMException('Quota','QuotaExceededError')};return;}
   if(mode==='corrupt')localStorage.setItem('saep.study.v1','{bad');
   if(mode==='legacy')localStorage.setItem('saep_progress',JSON.stringify({S01:{moduleId:'S01',status:'completed',score:100,questionsCompleted:10,questionsCorrect:10,attempts:10,hintsUsed:0,reviewQueue:[]}}));
  },mode);
  await page.goto(origin);await page.getByRole('heading',{name:'Sua trilha de estudo'}).waitFor();
  if(mode!=='quota')await page.locator('.storage-notice').waitFor();
  await page.getByRole('button',{name:/Ver plano S01:/}).click();await page.getByRole('button',{name:'Salvar para estudar',exact:true}).click();
  if(mode==='quota'||mode==='blocked')await page.locator('.storage-notice').waitFor();
  if(mode==='corrupt'&&await page.evaluate(()=>localStorage.getItem('saep.study.v1.previous'))!=='{bad')throw Error('Original corrompido perdido');
  if(mode==='legacy'&&await page.evaluate(()=>localStorage.getItem('saep_progress'))===null)throw Error('Registro legado apagado');
  if(errors.length)throw Error(errors.join(';'));await context.close();
 }
 console.log('35 temas, busca sem acentos, filtros, teclado, favoritos/reload, planos pendentes, storage corrompido/legado/bloqueado/quota e desktop/mobile passaram.');
}finally{await browser.close();}
