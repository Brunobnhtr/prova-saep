# Implementação incremental — orientação revisada

Estado atual: catálogo e planejamento, sem aulas/avaliações prontas. Ver `README.md` e a auditoria de 06/10/2026. Não tratar mensagens de entrega ou documentos históricos como aprovação do conteúdo.

## Próximo incremento: S01

1. Conferir as fontes de Segurança em Eletricidade e a edição vigente da norma, sem usar o checklist curto do MVP de motores como sequência normativa completa.
2. Produzir explicação curta, um cenário com estados/ordem verificáveis e questões originais por etapas. Segurança exige concluir o cenário sem pular passos.
3. Registrar fontes, edição, trechos, revisão técnica e limites pedagógicos. Usar assets provisórios claramente identificados enquanto faltarem os definitivos.
4. Implementar e testar avaliação de domínio e pré-requisitos no domínio, não apenas em botões. Meta provisória: 8/10 itens novos sem dica, raciocínio explicado; não é critério oficial do SAEP.
5. Só mudar `contentStatus` para `ready` quando o pacote pedagógico estiver implementado e revisado. Não criar botão de concluir manualmente um placeholder.
6. Mostrar a prévia ao usuário, ajustar e avançar um tema por vez.

## Sequência

A referência é `../docs/02-trilha-estudo.md` e `../data/fase2/mapa-conteudo.json`. A trilha começa S01 → S02 → F01 → M01 → F02. S01 e F01 não têm pré-requisitos, mas elegibilidade não implica conteúdo publicado. Não introduzir novos requisitos só para forçar uma fila única.

A prévia técnica de motores da raiz foi solicitada e autorizada anteriormente; preservar o trabalho e integrá-lo na etapa correspondente após revisão. Ela não substitui os fundamentos da trilha.

## Contratos que faltam antes de registrar aprendizagem

- Identidade/versão do conteúdo e da avaliação.
- Evidências de respostas, dicas, tentativas e conclusão do cenário.
- Regra de conclusão verificável, preservação de requisitos e reavaliação de conteúdo alterado.
- Persistência validada, migração por versão e exportação/importação.
- Revisão dos erros e progresso que represente domínio, não abertura de página ou quantidade de tentativas repetidas.

Guardar datas serializadas como strings ISO; reconstruir `Date` apenas para cálculos. Não duplicar estado derivável de progresso. Não copiar provas como se fossem questões originais nem apresentar a trilha editorial como matriz oficial.

## Acervo ampliado antes de produzir conteúdo

Consultar `../docs/09-acervo-ampliado-e-representacao-visual.md` e `../data/acervo-ampliado/cruzamento-35-temas.json`. Foram encontrados 93 dossiês e 9.791 questões externas, mas nenhum gabarito nos lotes. Dossiês são seleções automáticas com lacunas e falsos positivos, não conteúdo validado. Para S01, revisar 4.4/4.2 e a seleção de reenergização antes da aula. Manter as prioridades SAEP da coleta original separadas das frequências de concursos.

## Diretrizes editoriais recebidas

Ver `docs/10-processo-editorial-e-diagnostico.md` na raiz: validação progressiva, estados editoriais, proveniência, diagnóstico por etapas e V/F com justificativa. Antes de produção, apresentar candidatas/rejeitadas, resoluções e conversões. Nenhum gabarito preenchido em massa.
