# Fase 2 - Mapa de conteúdo e plano de estudo

Executada em 02/10/2026 após autorização explícita do usuário para concluir a conferência e iniciar esta fase. A arquitetura e a implementação ainda aguardam a aprovação prevista ao fim da Fase 2.

## Resultado

O acervo conferido tem **241 ocorrências em cinco documentos e 206 grupos conservadores**. Todas as ocorrências receberam um subtema principal em uma taxonomia editorial com **35 subtemas**. A classificação permite rastrear enunciado, fonte e página; não atribui códigos oficiais que não foram confirmados.

Entregáveis:

- [Conferência do acervo](00-conferencia-acervo-completo.md): correção do DOCX, alternativas gráficas e duplicatas.
- [Matriz de cobertura](02-matriz-cobertura.md): frequência por documento e grupo, dificuldade e prioridade.
- [Trilha de estudo](02-trilha-estudo.md): ordem por pré-requisitos, atividade e livros para cada subtema.
- [Conteúdos complementares](02-assuntos-fora-das-provas.md): assuntos curriculares não observados ou parcialmente cobertos.
- `data/fase2/mapa-conteudo.json`, `matriz-cobertura.csv`, `ocorrencias-classificadas.json` e `indice-deduplicado.json`: dados rastreáveis.
- `docs/verificacao-fase2.json`: conferência de contagens, livros e ausência de ciclos na trilha.

## Prioridades e método

A prioridade quantitativa usa frequência distinta × dificuldade média, com pesos 1/2/3. Nos 40 itens de S22 a dificuldade vem do rótulo impresso; nos demais é estimativa editorial de esforço, identificada nos dados. Não há resultados do aluno para medir dificuldade real. O maior peso do grupo é usado quando há ocorrências repetidas, evitando reduzir a prioridade pela repetição.

| Ordem por escore | Subtema | Escore |
|---:|---|---:|
| 1 | P01 - Condutores e fatores de correção | 36 |
| 2 | H02 - Sequências e diagnóstico eletropneumático | 26 |
| 3 | R02 - Subestações e barramentos | 25 |
| 4 | A02 - CLP e controle sequencial | 24 |
| 5 | E06 - Inversores e parametrização | 23 |
| 6 | P02 - Proteções, curvas e curto-circuito | 21 |

Segurança e fundamentos entram antes dessas prioridades porque sustentam a execução dos laboratórios. Itens contextuais podem mobilizar mais de um assunto; a matriz conta um subtema principal para não duplicar frequências. Temas de apoio aparecem nos pré-requisitos. A pontuação não é previsão estatística da próxima prova.

## Metas e cobertura curricular

Planejadas **542 questões originais** nos 35 subtemas observados, entre 8 e 24 por subtema; **64** em conteúdos curriculares complementares e uma reserva de **16** para motores de 9/12 pontas solicitados, condicionada a fonte técnica. São metas iniciais de produção nas fases futuras, não questões já disponíveis. Cada etapa de cálculo terá quatro alternativas; o mini-simulado poderá reproduzir o perfil de quatro ou cinco alternativas da fonte de estilo escolhida.

O currículo de referência vem dos planos oficiais CE e RR já coletados, com páginas de evidência no relatório complementar, e dos livros fornecidos. A unidade e o estado ainda não foram informados; a correspondência com o plano local está [VERIFICAR]. A eletrônica digital aparece como lógica no acervo, enquanto outros dispositivos merecem expansão curricular; Dahlander agora tem evidência no DOCX e não é mais uma lacuna total.

A taxonomia é Área > Tema > Subtema > item da Matriz. O último campo permanece `null` com [VERIFICAR] em todos os subtemas. Os cruzamentos de S22 ficam separados como rótulos impressos: não certificam uma matriz integral nem a edição vigente. Isso limita a afirmação de cobertura oficial, mas permite ordenar o estudo e preparar a arquitetura após aprovação.

## Próxima fase

Após aprovação, iniciar a Fase 3 e apresentar opções de stack, motor de simulação e fidelidade para escolha. O MVP de motores será tratado na Fase 4 com revisão de pré-requisitos. Ainda não foi escolhida tecnologia ou algoritmo.

## Resumo da Fase 2

1. DOCX conferido em 47 páginas e corrigido para 80 questões.
2. Acervo de cinco documentos: 241 ocorrências e 206 grupos conservadores.
3. Todas as ocorrências classificadas em 35 subtemas editoriais rastreáveis.
4. Frequências por documento, dificuldade e prioridades registradas.
5. Trilha ordenada por pré-requisitos, atividades e livros de apoio.
6. Metas: 542 questões observadas, 64 complementares e reserva de 16 para extensões.
7. Matriz oficial integral e currículo local permanecem [VERIFICAR].
8. Fase 2 concluída; Fase 3 aguarda aprovação do usuário.
