import {chromium} from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
try{for(const width of [1400,390]){
 const page=await browser.newPage({viewport:{width,height:1050}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:5173/');
 for(let i=1;i<=4;i++)await page.getByRole('button',{name:new RegExp(`^${i} ·`)}).click();
 await page.getByRole('button',{name:'Modo continuidade'}).click();
 const r=page.getByRole('button',{name:'Arrastar ponta vermelha'}),b=page.getByRole('button',{name:'Arrastar ponta preta'});await r.scrollIntoViewIfNeeded();const a=await r.boundingBox(),z=await b.boundingBox();await page.mouse.move(a.x+22,a.y+35);await page.mouse.down();await page.mouse.move(z.x+22,z.y+8,{steps:12});await page.mouse.up();
 for(const [x,y] of [[1,5],[2,6],[3,4]]){
 await page.getByRole('button',{name:'● Ponta vermelha',exact:true}).click();await page.locator(`[data-terminal="${x}"]`).click();await page.getByRole('button',{name:'● Ponta preta',exact:true}).click();await page.locator(`[data-terminal="${y}"]`).click();await page.getByRole('button',{name:'Aplicar etiquetas aos cabos'}).click();}
 await page.getByRole('button',{name:'Avançar para fechamento e rede'}).click();
 await page.getByRole('button',{name:'Ampliar placa e diagramas'}).click();await page.getByRole('dialog').waitFor();await page.getByRole('button',{name:'Fechar placa'}).click();
 await page.getByRole('button',{name:'Solicitar partida virtual'}).click();if(!await page.getByText('Partida bloqueada: falta conectar PE à carcaça.').count())throw Error('Partida incompleta permitida');
 async function wire(a,b){await page.locator(`[data-port="${a}"]`).click();await page.locator(`[data-port="${b}"]`).click();}
 if(width===1400){const a=await page.locator('[data-port=PE]').boundingBox(),b=await page.locator('[data-port=CASE]').boundingBox();await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:15});await page.mouse.up();if(await page.locator('.wire-list button').count()!==1)throw Error('Arraste não cria cabo');}
 for(const [x,y] of [['PE','CASE'],['L1','M1'],['L2','M2'],['L3','M3']])if(!(width===1400&&x==='PE'))await wire(x,y);
 await page.getByRole('button',{name:'Ponte entre bornes',exact:true}).click();await wire('M5','M6');await wire('M6','M4');if(await page.locator('.terminal-bridge').count()!==2)throw Error('Pontes estrela ausentes');
 await page.getByRole('button',{name:'Solicitar partida virtual'}).click();await page.getByText('Motor em funcionamento virtual · estrela · 380 V. Modelo ideal sem carga.').waitFor();
 if(await page.locator('.rotor.spinning').count()!==1)throw Error('Rotação ausente');if(!await page.locator('[data-port="M1"]').isDisabled())throw Error('Edição energizada');
 await page.screenshot({path:`output/previa/fechamento-${width}.png`,fullPage:true});
 await page.getByRole('button',{name:'Parar e isolar'}).click();await page.getByLabel('Tensão entre fases da fábrica').selectOption('220');await page.getByRole('button',{name:'Solicitar partida virtual'}).click();await page.getByText('Ligação estrela incompatível com a rede de 220 V e a placa Δ 220 / Y 380 V.').waitFor();
 while(await page.locator('.wire-list button').count())await page.locator('.wire-list button').first().click();
 await page.getByRole('button',{name:'Cabo pelas canaletas',exact:true}).click();
 for(const [x,y] of [['PE','CASE'],['L1','M1'],['L2','M2'],['L3','M3']])await wire(x,y);
 await page.getByRole('button',{name:'Ponte entre bornes',exact:true}).click();
 for(const [x,y] of [['M1','M4'],['M2','M5'],['M3','M6']])await wire(x,y);
 await page.getByRole('button',{name:'Solicitar partida virtual'}).click();await page.getByText('Motor em funcionamento virtual · triângulo · 220 V. Modelo ideal sem carga.').waitFor();
 if(await page.locator('.terminal-bridge').count()!==3)throw Error('Pontes triângulo ausentes');
 await page.screenshot({path:`output/previa/motor-triangulo-${width}.png`,fullPage:true});
 await page.getByRole('button',{name:'Parar e isolar'}).click();
 await page.getByRole('button',{name:'Ampliar placa e diagramas'}).click();await page.screenshot({path:`output/previa/placa-ampliada-${width}.png`});await page.getByRole('button',{name:'Fechar placa'}).click();
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Overflow da página');if(errors.length)throw Error(errors.join(';'));await page.close();
}console.log('Motor compartilhado, placa ampliada, arraste, pontes estrela/triângulo, partidas 380/220, proteção e layout desktop/móvel passaram.');}finally{await browser.close();}
