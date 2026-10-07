## 06/10/2026 — Contratos editoriais e V/F

Consolidados os dois anexos em `10-processo-editorial-e-diagnostico.md`, com taxonomia e schema fora da aplicação. Fontes recebidas preservadas em `docs/editorial/`. Nenhum item resolvido/publicado nem mudança no código de produção.

## 06/10/2026 — Acervo externo ampliado, antes de iniciar S01

Inventariados 93 dossiês/4.080 figuras e 9.791 questões dos 49 lotes externos. Sem gabaritos nos lotes; lacunas e seleção temática precisam de revisão. Cruzamento candidato com os 35 módulos salvo em `data/acervo-ampliado/`; recomendação Schemdraw/SVG para esquemas, Matplotlib para curvas e KaTeX para fórmulas. Nenhum novo módulo iniciado nem acervo externo alterado. Relatório: [09-acervo-ampliado-e-representacao-visual.md](09-acervo-ampliado-e-representacao-visual.md).

## 06/10/2026 — Auditoria e revisão da base de estudo

Conferida e corrigida a entrega `plataforma-saep`: 35 temas/542 metas corretos, mas sem aulas ou avaliação. Novo design, busca/filtros, favoritos, persistência defensiva, tipos estritos, português e publicação separada de pré-requisitos. Catálogo em 5174; laboratório da raiz preservado em 5173. Conclusões antigas não liberam requisitos sem evidência. Sete testes de domínio, build, lint e testes Chrome desktop/viewport móvel passando. Próximo incremento: S01, um tema por revisão. Relatório em [08-auditoria-plataforma-2026-10-06.md](08-auditoria-plataforma-2026-10-06.md).

## Revisão: fechamento na própria caixa do motor e placa de referência

MotorScene compartilhado entre identificação e fechamento; seis posições com disposição W2/U2/V2 acima e U1/V1/W1 abaixo. A montagem passa a exibir o motor azul com sua caixa, preservando as etiquetas e os pares. Cabos externos continuam nas canaletas; ferramenta de ponte desenha barramentos diretamente entre bornes, com o mesmo grafo de avaliação. Placa didática ampliável (dialog nativo, fechamento Escape/botão), dados 220/380 V, 60 Hz, diagramas explícitos Δ 220 e Y 380. Não copia marca nem a ficha de um produto real. Referência: placa preta de seis pontas enviada pelo usuário; a branca tem doze pontas e não integra este cenário.

Distinguir etiqueta do aluno (número arbitrário) da posição de referência U1…W2. Seletor de posicionamento troca cabos entre posições antes da montagem, preservando unicidade; com conexões montadas, reposicionamento bloqueado até removê-las. Numeração sequencial de pares 1–2,3–4,5–6 não é automaticamente identificação normalizada U1/U2 etc. Continuidade sozinha não prova orientação. Avaliação de partida é virtual, com proteção didática, e não é procedimento para testar ligações incertas em equipamento real. Este tema é partida direta com fechamento pela placa, não chave automática estrela-triângulo.

Verificação: build, seis testes de domínio, regressão do instrumento, UI até partida estrela 380 e triângulo 220 com pontes físicas, arraste, parada, tensão incompatível e placa ampliada; larguras 1400/390. Fotos/modelos detalhados permanecem pendentes. Diagrama usa rolagem horizontal no celular.

Plataformas: recomendação para possível evolução 3D web é Babylon.js com TS e React para conteúdo; Capacitor permite empacotar para Android, PC inicialmente navegador/PWA (PWA ainda não implementada). Nenhuma migração ou APK nesta entrega. Godot continua opção forte para Android e Windows nativos, com ressalvas específicas de exportação web. Fontes: https://www.babylonjs.com/specifications/ ; https://capacitorjs.com/docs ; https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html ; https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_windows.html . A escolha futura depende de protótipo com assets e teste no aparelho, não da aparência do CSS atual.

## Prévia 02: montagem, rede e partida virtual

Refatorada a composição para painel industrial escuro, motor maior e instrumento compacto. Após seis etiquetas, abre a montagem separada: placa didática Δ 220 V / Y 380 V, rede selecionável 220/380 V entre fases, L1/L2/L3/PE, carcaça, quatro conectores J e cabos com as etiquetas do aluno. Arraste entre portas ou clique em origem/destino; rastro durante arraste. Canaletas ortogonais, remoção na lista; cruzamento não conecta. Cada J representa conector multipolar com contato comum, sem simulação de decapagem/aperto. Retornar à identificação descarta a montagem da etapa.

Motor de validação em TS puro usa grafo das conexões e orientação interna dos três enrolamentos. Reconhece estrela/triângulo equivalentes, recusa fases unidas, contato com PE/carcaça, PE ausente, topologia incompleta, orientação incompatível e tensão errada para a placa. Troca de fases não é tratada como inversão de bobina. Modelo ideal sem carga, sem cálculo de corrente, aquecimento, torque ou proteção real. Falhas bloqueiam a partida; não simula prática de energizar ligações suspeitas em instalação real. Animação de rotor e percurso apenas na partida aceita; montagem bloqueada até parar/isolar. Multímetro pertence exclusivamente à etapa isolada e para seu som ao avançar.

Validação: seis testes de domínio, testes de instrumento, percurso de três pares até partida estrela, arraste de cabo desktop, rede incompatível, parada e edição, larguras 1400/390 sem overflow. Triângulo validado no domínio. Assets permanecem provisórios; ainda faltam imagens detalhadas e visualização espacial dos equipamentos. Diagrama móvel tem rolagem horizontal deliberada.

Godot: avaliadas as docs oficiais https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html (04/10/2026). Exportação web exige WebAssembly/WebGL2, renderizador Compatibility e considera limitações móveis. Manter React/TS neste incremento; eventual laboratório 3D em Godot deve ser comparação de protótipos no aparelho do usuário antes de migração. Referência de relação tensão/ligação: guia WEG https://static.weg.net/medias/downloadcenter/hc0/he9/WEG-soft-starter-manual-usass11-brochure-english.pdf. Placa do cenário é didática, não ficha técnica de produto.

## Revisão: etiquetas individuais dos cabos

Ao medir dois cabos distintos com continuidade, a bancada abre automaticamente dois seletores de etiquetas de 1 a 6, um para cada ponta do instrumento. As etiquetas são escolhas do aluno, editáveis pelo registro; não representam validação de início/fim ou polaridade. Impede apenas etiquetas duplicadas no mesmo cabo/par ou em outros cabos. Não há acerto, check de correção ou missão concluída. Continuidade confirma um caminho elétrico no cenário, não a orientação do enrolamento.

Escopo desta revisão: identificação e etiquetagem. Fechamento e partida permanecem pendentes da revisão deste cenário. Planejar outros métodos em etapa posterior, com fontes técnicas e condições de segurança; não usar partida experimental como confirmação automática de ligação segura. Testes de interface passaram em 1400 e 390 px: abertura automática, etiquetas independentes (inclusive ordem invertida), edição após mudar medição, seleção persistente e bip contínuo/parada.

# Progresso - Plataforma de estudo SAEP

Atualizado em 02/10/2026. Técnico em Eletrotécnica; Android modesto e PC, offline e acessível.

## Feito

- Instrumento revisado conforme usuário: só continuidade, sem botão artificial de teste; seleção de ponta persistente; bip contínuo; bornes sem números até identificação pelo aluno. Build, domínio e teste E2E de contato/áudio/numeração passaram. Teste atualizado: `node scripts/testar-multimetro.mjs`.

- Corrigido teste das pontas: contato físico por arraste agora é detectado e conclui teste em modo continuidade após preparo; visor e legenda respondem ao contato/separação. Build, domínio, teste de contato e regressão de arraste passaram.

- Arraste real das pontas adicionado à prévia, com encaixe em bornes, desconexão ao soltar fora, cabos acompanhando gesto e missão/progresso de três bobinas. Manipulação permitida desde o início; medição depende do preparo. Build, testes e arraste automatizado passaram no Chrome desktop e largura móvel; Android físico ainda pendente. Aguardando revisão desta mesma bancada antes de ampliar.

- Revisão da primeira prévia: corrigido bloqueio pouco claro, instruções acima da bancada e feedback imediato; adicionados condutores do motor e cabos das pontas visíveis. Medição continua bloqueada até preparo/teste. Sem troca de stack; assets detalhados e arraste ainda pendentes. Build, testes de domínio e navegador passaram após correção.

- 04/10/2026: acolhido o conjunto recomendado com condições de assets provisórios identificados e preparo seguro. Primeira prévia React/TypeScript/Vite criada: motor de seis pontas, grafo independente, multímetro, teste de pontas e registro dos pares. Build e testes de domínio passaram. Detalhes em `04-previa-01.md`; aguardando revisão antes de ampliar. Os estados pendentes da proposta abaixo são históricos.

- Atualização de 04/10/2026: requisito de assets detalhados para motores, componentes e ferramentas e de entrega por exemplos pequenos registrado em `docs/arquitetura/07-assets-e-revisao-visual.md`. Primeiro exemplo proposto: motor de seis pontas e multímetro virtual para continuidade. Mostrar e revisar antes de ampliar; comunicar assets faltantes e pesquisar programas/fontes concretos quando necessário. Esta atualização não aprova stack/algoritmo/fidelidade nem inicia implementação.

- Fases 0/1 concluídas e pesquisa ampliada para sites públicos autorizada.
- Acervo ampliado conferido: quatro PDFs e um DOCX, 241 ocorrências e 206 grupos conservadores. Dois gabaritos de 40 respostas preservados; respostas dos demais não inferidas.
- DOCX de 2023: 47 páginas conferidas no Word em modo somente leitura e 80 itens recuperados; questão 11 curta corrigida. Quatro itens têm alternativas gráficas. Mídias preservadas; repetição 3/61 consolidada na frequência, sem transferir letra de gabarito.
- Simulado 2022.2: 40 IDs distintos, dificuldades e cruzamentos impressos preservados. Sem ID compartilhado com A1/A2.
- Dois planos oficiais, quatro páginas oficiais e um manual público operacional coletados; não contados como provas.
- 76 livros SENAI, 15.161 páginas, inventariados e extraídos. Originais preservados.
- Cinco PDFs autorais para o usuário enviar ao Scribd; excluídos da frequência das provas.
- Fase 2 explicitamente autorizada e concluída: 35 subtemas, cobertura, dificuldades, prioridades, pré-requisitos, atividades, livros e conteúdos complementares.
- Metas de produção futura: 542 questões nos temas observados, 64 complementares e reserva de 16 para motores 9/12 pontas. Não são questões já produzidas.
- Entregáveis em 00-conferencia-acervo-completo.md, 02-mapa-conteudo.md, 02-matriz-cobertura.md, 02-trilha-estudo.md e 02-assuntos-fora-das-provas.md. Dados em data/fase2/ e verificação em docs/verificacao-fase2.json.

## Próximo somente após aprovação

**Atualização:** o usuário autorizou continuar para a Fase 3. A proposta foi preparada em `docs/arquitetura/README.md`, com requisitos, três opções de stack/algoritmo/fidelidade, componentes, schemas, motores, estratégia offline, testes e roadmap. As três escolhas estão pendentes nos ADRs 001-003; recomendações não foram registradas como decisões aceitas. Nenhum aplicativo criado. O próximo passo atual é receber essas escolhas, consolidar a arquitetura e apresentar o encerramento da Fase 3 para aprovação antes do MVP. A lista abaixo conserva o plano de transição da Fase 2.

1. Receber aprovação da Fase 2 para iniciar a Fase 3.
2. Confirmar unidade/estado e plano local quando disponíveis; data da prova e horas de estudo permitem ajustar calendário.
3. Elaborar requisitos e arquitetura; apresentar opções de stack, algoritmo e fidelidade com recomendação, aguardando escolha nas decisões com trade-offs.
4. Parar ao fim da Fase 3. MVP de motores apenas na Fase 4 após aprovação.

## Limitações e pendências

- Matriz integral específica não confirmada; códigos oficiais permanecem null e [VERIFICAR]. Cruzamentos antigos não equivalem à matriz vigente.
- Unidade/estado e currículo local desconhecidos. Planos CE/RR são referências comparativas.
- Ano e aplicação nacional dos documentos não certificados.
- Dificuldade impressa em S22 e editorial nos demais; desempenho do aluno ainda desconhecido.
- Deduplicação conservadora: comandos/opções diferentes ficam separados; outras variantes semânticas podem existir.
- Revisão técnica integral das respostas, transcrição e descrição acessível dos diagramas pendentes para os módulos. Anotações e setas não foram certificadas como gabarito.
- Alertas normativos do diagnóstico mantidos; questão 69 do DOCX menciona 5410/2015 para SPDA e exige conferência.
- 1.286 páginas dos livros têm pouco texto. Capítulos, versões e dados técnicos serão validados ao produzir conteúdo.
- Direitos de publicação dos materiais de terceiros não confirmados; versão compartilhada deve usar conteúdo original.

## Retomada e reprodução

Ler 02-mapa-conteudo.md e relatórios vinculados. Scripts: extrair_docx_saep.py, conferir_acervo_fase2.py e gerar_fase2.py, nessa ordem. A conferência requer tmp/pdfs/colecao-2023-conferencia.pdf, exportado do Word em modo somente leitura. extrair_simulado_2022.py reproduz a extração do PDF novo. Scripts iniciais preservam o diagnóstico histórico dos três PDFs. Não repetir downloads ou extração de todos os livros sem necessidade.

Aguardar aprovação ao fim das Fases 2, 3, 4 e de cada módulo da Fase 5. Não iniciar arquitetura ou implementação antes da aprovação correspondente.
