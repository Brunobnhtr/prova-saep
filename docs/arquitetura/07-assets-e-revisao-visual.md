# Assets detalhados e construção por exemplos

Atualização de 04/10/2026 solicitada pelo usuário. Imagens de alta fidelidade visual são requisito do projeto. Essa exigência não escolhe a fidelidade física da simulação nem a stack pendentes.

## Aparência e animação

Motores, componentes e ferramentas devem ser reconhecíveis, detalhados e proporcionais, com terminais, seletores, bornes e inscrições legíveis nas vistas necessárias. Uma foto bonita não basta: a representação deve permitir identificar e operar o componente no laboratório.

Usar imagem detalhada para carcaça/corpo e camadas independentes para fios, pontes, terminais, ponteiros, seletor, contatos e movimento. Fotografias ou renders podem compor o corpo; SVG pode fornecer conexões e áreas de interação. O asset não define a regra elétrica. Placa, quantidade de terminais e posição das conexões precisam de revisão técnica.

Vistas iniciais propostas: motor externo e caixa de bornes aberta; multímetro frontal com visor e seletor; pontas de prova e cabos. Quando o tema exigir, acrescentar contator, disjuntor-motor e relé térmico. Cada ferramenta/componente efetivamente usado em um tema terá seu inventário de assets; não baixar toda uma biblioteca antes de saber quais vistas são necessárias.

## Obtenção e registro

Ordem de trabalho: conferir o acervo existente; procurar imagens/modelos com permissão de uso adequada; produzir desenhos/renders originais ou fotografias próprias; usar geração de imagem quando apropriado e revisar a precisão técnica. Imagens geradas não certificam terminais, símbolos ou placas. Não tratar imagens dos livros como automaticamente liberadas para publicação.

Para cada asset registrar ID, componente/modelo, vista, origem, autor, licença/permissão, uso local ou compartilhável, arquivo mestre, versão otimizada, dimensões, camadas móveis, pontos de conexão e status da revisão técnica. Conservar o mestre detalhado e servir versões menores conforme tela/zoom; baixar imagens por tema. Medir o impacto no orçamento de 5 MB proposto, revendo-o se necessário com o usuário, sem sacrificar legibilidade dos bornes.

Se faltar um asset, informar especificamente o componente, vista, camadas/formato e impedimento. Antes de sugerir instalação, pesquisar opções atuais e apresentar links, exportação suportada, licença e utilidade. O usuário pode fornecer fotos, modelos ou arquivos que tenha autorização para reutilizar.

Aplicativos/APKs não são a fonte padrão: extrair um arquivo de um pacote não concede permissão para reutilizá-lo, e uma textura isolada pode não conter as vistas ou partes necessárias. Avaliar um programa concreto pela licença dos assets e capacidade de exportação antes de pedir que o usuário baixe ou de extrair seus recursos. Preferir arquivos disponibilizados para uso/exportação e conteúdo próprio.

## Primeiro exemplo e pontos de revisão

Após consolidar e aprovar a Fase 3, iniciar somente um exemplo do tema Motores elétricos: **identificação das bobinas de um motor trifásico de seis pontas com multímetro virtual**, precedido do estado seguro do cenário. O exemplo proposto contém uma explicação curta, motor/caixa de bornes, instrumento e uma interação de continuidade. Não incluir todos os fechamentos, partidas e temas nessa primeira entrega.

Mostrar o exemplo executável para o usuário revisar aparência, escala, legibilidade, interação e feedback. Registrar as alterações pedidas e aplicar antes de ampliar. Se o asset final não estiver disponível, informar a pendência e identificar qualquer representação provisória na prévia; não apresentá-la como a versão de alta fidelidade concluída.

Após aprovação do exemplo, avançar em incrementos: placa e rede; fechamento e comando; falhas e proteção; questões por etapas; mini-simulado e progresso. Cada incremento terá prévia e ponto de revisão antes do seguinte. A fatia completa exigida na Fase 4 continua sendo o objetivo final, construída por essas entregas pequenas.

Nenhum aplicativo, asset definitivo ou exemplo executável foi criado nesta atualização documental. Stack, algoritmo e fidelidade física continuam aguardando escolha explícita.

## Referência visual fornecida: placas de seis e doze pontas

A placa preta enviada nesta revisão é referência para o cenário de seis pontas: W2/U2/V2 acima, U1/V1/W1 abaixo, Δ 220 / Y 380. A branca tem 12 pontas e exige outro modelo. Implementada placa didática ampliável com diagramas, sem atribuição falsa a WEG. Reutilizar a mesma representação do motor entre medir e montar; pontes dentro da caixa de bornes, cabos externos nas canaletas. Ainda faltam modelo/render detalhado da carcaça e caixa aberta, textura de metal da placa e terminais/pontes reconhecíveis em zoom.

Para eventual 3D web, estudar Babylon.js com fallback WebGL; para instalação Android, Capacitor ou Godot nativo conforme protótipo. Ainda não escolhida migração nem instalados SDKs. Uma engine não substitui os assets e a revisão elétrica.

## Acervo e renderização — revisão de 06/10/2026

O acervo externo traz 4.080 figuras dos dossiês e 2.861 arquivos de imagens das questões. Inventário e cruzamento editorial em `data/acervo-ampliado/` na raiz. Figuras e respostas não são tecnicamente validadas pela extração; conferir especialmente imagens faltantes, enunciados dependentes de figuras e gabaritos ausentes.

Proposta: Schemdraw gera esquemas originais em SVG na preparação; Matplotlib gera curvas/gráficos. SVG/Canvas em TypeScript fornece a interação no navegador e usa regras/topologia separadas. KaTeX renderiza fórmulas em sintaxe LaTeX, com MathJax como alternativa conforme comandos. Dependências/fixtures locais serão avaliadas no primeiro exemplo, sem prometer backend Python ou Pyodide no celular. Isso não substitui fotos/renders de equipamentos. Nenhuma dessas novas dependências foi instalada nesta etapa.
