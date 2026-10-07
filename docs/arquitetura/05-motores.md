# Motores de simulação, questões e revisão

## Simulação proposta

Interface lógica: `step(estado, ação, tempoSimulado) → novoEstado + eventos`. A implementação concreta depende da escolha do algoritmo. Rede elétrica, proteção, procedimento de segurança e animação são partes distintas. A fonte é descrita por tensão, frequência e sequência de fases; bobinas por família, terminais e parâmetros verificados.

No algoritmo recomendado, construir componentes conectados e distinguir fios, contatos, bobinas, alimentação e proteção. Avaliar curto, falta de fase, alimentação incompatível, fechamento estrela/triângulo, sequência e intertravamento antes de permitir a energização do cenário. Não considerar uma ligação correta só porque coincide com coordenadas ou com ordem de criação dos fios.

| Situação | Comportamento pedagógico a implementar | Limite técnico |
|---|---|---|
| Ligação compatível e fases presentes | Partida e rotação segundo o cenário | Corrente/carga nominais apenas com placa/modelo validado |
| Sequência de fases invertida | Sentido invertido no motor suportado | Não tratar toda inversão de bobina como mera troca de fase |
| Fase ausente | Distinguir motor parado de motor já em movimento, carga e proteção | Não impor um único resultado universal para todas as condições |
| Tensão/fechamento incompatível | Falha de partida, corrente e calor conforme regra verificada | Sem valores numéricos inventados para qualquer motor |
| Bobina invertida/erro nos terminais | Diagnóstico específico da família | Polaridade e geometria precisam de fonte própria |
| Selo/intertravamento incorreto | Contator não mantém operação ou conflito detectado | Proteção/tempo dependem do cenário |
| Sobrecarga persistente | Aquecimento didático e atuação de proteção | Índice de calor não deve ser rotulado como temperatura real |

No modo estudo, identificar causa e sugerir inspeção. No modo prova, mostrar os sinais sem revelar a resolução. O erro de procedimento deve produzir um evento de risco e bloqueio pedagógico; não usar animação de dano físico a pessoas. A consequência elétrica, quando aplicável, precisa de condição de energização definida.

Sequência de segurança completa será baseada no texto normativo verificado, incluindo etapas além de seccionar/impedir/constatar. Isso é conteúdo técnico pendente, não decisão de interface. Para motores de 9/12 pontas e Dahlander, usar modelos separados e diagramas próprios revisados.

## Motor de perguntas

1. Selecionar template e versão; criar semente reproduzível.
2. Gerar parâmetros dentro de faixas e hipóteses verificadas.
3. Calcular resposta e resultados de erros típicos registrados em código.
4. Filtrar valores inválidos e colisões de alternativas após arredondamento.
5. Ordenar opções por uma permutação salva, com IDs estáveis.
6. Ao acertar, liberar a etapa seguinte com substituição dos valores; ao errar, feedback do erro e dica opcional.
7. Ao concluir, mostrar resultado com unidade e solução completa.

Não gerar alternativas por textos aleatórios desconectados do raciocínio. Erros como esquecer fator trifásico, confundir entrada/saída ou unidade só entram onde a hipótese física e a fórmula forem válidas. Resposta precisa ser única na tolerância definida para unidade/arredondamento. Questões paramétricas não recebem valores “corretos” digitados manualmente como fonte da verdade; exemplos resolvidos são fixtures independentes de teste.

Mini-simulado: perfil explícito de 4 ou 5 opções, seleção balanceada por cobertura, sem duplicata de template com os mesmos parâmetros. Deadline salvo; retomada não reinicia o cronômetro. Ao entregar/expirar, congelar respostas e gerar resumo por subtema. Códigos da matriz só serão exibidos como oficiais após confirmação.

## Áudio e equivalência visual

Proposta: criar AudioContext apenas após ação do aluno; volume limitado e botão para silenciar; reutilizar contexto e desconectar nós ao sair. Modelar estado semântico (“zumbido”, “vibração”, “proteção atuou”) antes de som e desenho. Uma base sonora de 60 Hz com harmônicos será apenas efeito didático nos cenários dessa frequência, nunca inferida como espectro acústico real do motor. Inversor/rede em outra frequência exigem efeito coerente e identificado.

Cada evento tem rótulo textual, intensidade visual e causa no modo estudo. Rotor e indicador de temperatura acompanham estado. Respeitar redução de movimento; leitor de tela anuncia mudanças relevantes, não cada frame. Legendas continuam com som desligado. [Web Audio: boas práticas e reprodução após interação](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices).

## Progresso e revisão

Salvar conclusão, primeiro acerto, tentativas, dicas e erros por subtema. Não considerar acerto após várias dicas como domínio igual ao primeiro acerto. A fila inicial proposta combina erro recente, atraso da revisão e pré-requisito.

Heurística proposta: erro retorna na próxima sessão; acerto sem dica progride em intervalos configuráveis de 1, 3, 7 e 14 dias; novo erro reduz o intervalo. A versão do scheduler e a data-alvo são salvas. Não é promessa de algoritmo científico otimizado. Comparação com fator de facilidade ou algoritmo probabilístico pode ser feita antes de alterar o agendamento.
