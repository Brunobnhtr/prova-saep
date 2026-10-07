import {chromium} from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 for(const width of [1400,390]){
  const page=await browser.newPage({viewport:{width,height:1000}});
  await page.addInitScript(()=>{
   window.toneCount=0;const start=OscillatorNode.prototype.start,stop=OscillatorNode.prototype.stop;
   OscillatorNode.prototype.start=function(...a){window.toneCount++;return start.apply(this,a)};
   OscillatorNode.prototype.stop=function(...a){window.toneCount--;return stop.apply(this,a)};
  });
  await page.goto('http://127.0.0.1:5173/');
  if(await page.getByRole('button',{name:'Unir pontas e testar instrumento'}).count())throw Error('Botão de teste permanece');
  if((await page.locator('.winding-label').allTextContents()).some(t=>t.trim()))throw Error('Bornes numerados inicialmente');
  for(let i=1;i<=4;i++)await page.getByRole('button',{name:new RegExp(`^${i} ·`)}).click();
  await page.getByRole('button',{name:'Modo continuidade'}).click();
  const red=page.getByRole('button',{name:'Arrastar ponta vermelha'}),black=page.getByRole('button',{name:'Arrastar ponta preta'});
  await red.scrollIntoViewIfNeeded();let a=await red.boundingBox(),b=await black.boundingBox();
  await page.mouse.move(a.x+22,a.y+35);await page.mouse.down();await page.mouse.move(b.x+22,b.y+8,{steps:12});await page.mouse.up();
  await page.getByText('BAIXA R',{exact:true}).waitFor();
  await page.waitForTimeout(600);
  if(await page.evaluate(()=>window.toneCount)!==1)throw Error('Bip não permaneceu ativo');
  await page.getByRole('button',{name:'● Ponta vermelha',exact:true}).click();
  await page.locator('[data-terminal="1"]').click();
  await page.locator('[data-terminal="2"]').click();
  if(!await page.locator('[data-terminal="2"]').getAttribute('class').then(s=>s.includes('red')))throw Error('Ponta selecionada muda automaticamente');
  if(await page.getByRole('button',{name:'● Ponta preta',exact:true}).getAttribute('aria-pressed')!=='false')throw Error('Seleção preta automática');
  await page.locator('[data-terminal="1"]').click();
  await page.getByRole('button',{name:'● Ponta preta',exact:true}).click();
  await page.locator('[data-terminal="5"]').click();
  await page.getByText('BAIXA R',{exact:true}).waitFor();
  await page.waitForTimeout(600);if(await page.evaluate(()=>window.toneCount)!==1)throw Error('Bip da bobina não contínuo');
  await page.getByRole('region',{name:'Numerar os dois cabos'}).waitFor();
  await page.getByLabel('Número do cabo na ponta vermelha').selectOption('2');
  await page.getByLabel('Número do cabo na ponta preta').selectOption('1');
  await page.getByRole('button',{name:'Aplicar etiquetas aos cabos'}).click();
  if(await page.locator('[data-terminal="1"] .winding-label').textContent()!=='2'||await page.locator('[data-terminal="5"] .winding-label').textContent()!=='1')throw Error('Etiquetas individuais não aplicadas');
  await page.getByRole('button',{name:'Cabos 2 e 1 · editar etiquetas'}).click();
  await page.getByLabel('Número do cabo na ponta vermelha').selectOption('6');
  await page.getByLabel('Número do cabo na ponta preta').selectOption('5');
  await page.getByRole('button',{name:'Aplicar etiquetas aos cabos'}).click();
  await page.locator('[data-terminal="2"]').click();
  await page.getByRole('button',{name:'Cabos 6 e 5 · editar etiquetas'}).click();
  await page.getByRole('region',{name:'Numerar os dois cabos'}).waitFor();
  await page.getByRole('button',{name:'Aplicar etiquetas aos cabos'}).click();
  await page.locator('[data-terminal="2"]').click();await page.getByText('OL',{exact:true}).waitFor();
  await page.waitForTimeout(100);if(await page.evaluate(()=>window.toneCount)!==0)throw Error('Som não parou ao abrir circuito');
  await page.screenshot({path:`output/previa/multimetro-ajustado-${width}.png`,fullPage:true});
  await page.close();
 }
 console.log('Modo único, teste por contato, seleção persistente, bip contínuo e parada, etiquetas individuais automáticas e edição sem validação de polaridade passaram em desktop e largura móvel.');
}finally{await browser.close();}
