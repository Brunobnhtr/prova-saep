# ADR 002 - Algoritmo da simulação

Data: 02/10/2026. Status: **proposta; aguardando escolha do usuário**.

Contexto: aluno conecta fios livremente, identifica bobinas e observa consequências de erros. A comparação de desenho não basta para reconhecer equivalência elétrica.

Alternativas: A grafo de ligações com regras e estados; B somente cenários por regras; C análise fasorial e circuito equivalente por fase. Comparação em [opções](../02-opcoes-e-decisoes.md).

Recomendação: A. Grafo reconhece conectividade, regras interpretam família/condições e estados registram segurança/operação. Consequências: regras técnicas precisam de revisão; não é solver genérico e não produz toda grandeza automaticamente. B restringe exploração; C exige parâmetros e validação de domínio, sem resolver sozinho a dinâmica de partida.

Decisão final: pendente. A API de domínio proposta é independente da escolha e da UI.
