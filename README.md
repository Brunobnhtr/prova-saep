## Revisão — mesmo motor e placa com diagramas

A montagem agora ocorre na caixa de bornes da mesma representação do motor usada na identificação. Placa didática ampliável com Δ 220 / Y 380, ferramentas de cabos e pontes, posições U1…W2 e etiquetas individuais do aluno. Testes incluem ambos os fechamentos na interface. Assets seguem provisórios; sem APK ou engine 3D nesta revisão.

## Prévia 02 — montagem interativa

Identifique e etiquete os seis cabos, avance para o fechamento, confira a placa e a tensão da rede e monte conexões arrastando ou clicando nas portas. J1–J4 são conectores de emenda; remova cabos na lista. A partida virtual ideal valida estrela/triângulo, tensão e orientação; pare/isole antes de editar. Assets provisórios. Testes: `npm test`, `node scripts/testar-multimetro.mjs`, `node scripts/testar-fechamento.mjs`. A montagem é descartada ao retornar à identificação.

# Bancada SAEP - Primeira prévia

React, TypeScript e Vite. Exemplo inicial: motor trifásico de seis pontas isolado e multímetro virtual para continuidade. Assets ilustrados provisórios explicitamente identificados. Não representa motor de fabricante nem valor de resistência real.

## Executar

Node instalado; executar `npm install`, depois `npm run dev`. Abrir o endereço exibido no terminal. `npm run build` valida TypeScript e gera `dist/`; `npm run preview` serve o build. `npm test` verifica o domínio. `node scripts/verificar-previa.mjs` verifica a interação usando Chrome instalado e servidor na porta 5173.

## Fluxo

Revisão atual: apenas botão de continuidade; teste unindo as pontas fisicamente por arraste. Som contínuo habilitado por padrão e silenciável. Clique nos bornes mantém a ponta selecionada; mude explicitamente no botão da outra ponta. Os bornes não mostram números inicialmente: após medir um par, escolha a numeração da bobina e clique em Identificar bobina. Teste atual: `node scripts/testar-multimetro.mjs`.

Agora é possível pegar e arrastar as duas pontas físicas na bancada com mouse ou toque. Solte a ponta sobre um borne para encaixar; solte fora dos bornes para desconectar. Os botões de seleção permanecem como alternativa por teclado. A missão indica os pares encontrados. Manipulação é liberada antes do preparo, mas medição continua bloqueada até o teste do instrumento. `node scripts/testar-arraste.mjs` verifica esse fluxo.

Completar as quatro confirmações do cenário isolado; selecionar continuidade; unir pontas e testar; selecionar ponta e terminal; registrar os três pares. Botões operam por teclado/toque. Som opcional, com feedback visual. A continuidade não identifica polaridade. As confirmações não substituem a NR-10 completa.

Esta prévia não tem energização, corrente/calor, prova, persistência ou service worker offline. Esses incrementos aguardam revisão. Nenhum conteúdo de terceiros entra no build.

## Assets faltantes

Motor externo e caixa de bornes aberta, sem pontes, em vistas compatíveis; multímetro frontal detalhado com visor/seletor em camadas; pontas de prova e cabos. Precisam de fonte/permissão e revisão de terminais. Os desenhos atuais são autorais provisórios em CSS. Fotos próprias desses objetos podem servir de referência; não é preciso instalar aplicativos/APKs agora.
