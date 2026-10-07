# 📚 Plataforma SAEP - Técnico em Eletrotécnica

## 🎯 Sobre o Projeto

Plataforma de estudos interativa para preparação da prova SAEP (Sistema de Avaliação da Educação Profissional) do curso Técnico em Eletrotécnica do SENAI.

**Status atual:** Estrutura base implementada - Pronta para implementação incremental de conteúdo pedagógico

## 📋 Características Principais

### ✅ Implementado

- **35 Módulos organizados** seguindo a trilha de estudos oficial (docs/02-trilha-estudo.md)
- **Sistema de pré-requisitos** - Módulos desbloqueiam conforme progresso
- **Ordem pedagógica**: Do básico ao avançado (Segurança → Fundamentos → Intermediário → Avançado)
- **Priorização por matriz**: Baseado na frequência × dificuldade das provas reais
- **Interface responsiva** - Desktop e Mobile
- **Sistema de progresso** com localStorage
- **Arquitetura React + TypeScript + Vite** (stack aprovado)
- **Estrutura de dados** completa e tipada

### 🚧 Aguardando Implementação Incremental

Cada módulo seguirá o ciclo pedagógico completo:

1. **Explicação curta** → Conceitos fundamentais
2. **Atividade/Laboratório** → Prática específica do tema
3. **Questões por etapas** → 4 alternativas calculadas com feedback
4. **Revisão espaçada** → Sistema inteligente de reforço

**Laboratórios virtuais** (quando aplicável):
- Multímetro e instrumentos
- Circuitos virtuais
- Diagramas interativos
- Simulações de componentes

## 🗺️ Trilha de Estudos (35 Módulos)

### 📍 Módulos Iniciais (Sempre disponíveis)

1. **S01** - Desenergização e reenergização (Segurança)
2. **F01** - Unidades e grandezas CC/CA (Fundamentos)

### 🔐 Módulos com Pré-requisitos

Exemplo de progressão:
- S01 → S02 (Segurança EPI)
- F01 → M01 (Multímetro)
- F01 → F02 (Lei de Ohm) → F03 (Reatância) → F04 (Potência)
- E01 → E02 → E03 → E04/E06 (Motores e Comandos)

### 🎯 Módulos de Alta Prioridade (Top 6)

1. **P01** - Condutores e fatores de correção (Prioridade 36)
2. **H02** - Diagnóstico eletropneumático (Prioridade 26)
3. **R02** - Subestações (Prioridade 25)
4. **A02** - CLP e controle sequencial (Prioridade 24)
5. **E06** - Inversores e parametrização (Prioridade 23)
6. **P02** - Proteções e curto-circuito (Prioridade 21)

## 🚀 Como Executar

### Pré-requisitos

- Node.js 18+ instalado
- npm ou yarn

### Instalação

```bash
# Entre na pasta do projeto
cd plataforma-saep

# Instale as dependências (já instaladas)
npm install

# Execute em modo desenvolvimento
npm run dev
```

### Acesso

Abra o navegador em: `http://localhost:5173`

## 📁 Estrutura do Projeto

```
plataforma-saep/
├── src/
│   ├── components/          # Componentes React
│   │   ├── ModuleCatalog.tsx    # Catálogo de módulos
│   │   ├── ModuleDetail.tsx     # Detalhes e estudo
│   │   └── ProgressBar.tsx      # Barra de progresso
│   ├── data/
│   │   └── modules.ts           # 35 módulos configurados
│   ├── types/
│   │   └── index.ts             # Tipos TypeScript
│   ├── hooks/                   # Hooks customizados (futuro)
│   ├── modules/                 # Conteúdo pedagógico (futuro)
│   ├── utils/                   # Utilitários (futuro)
│   ├── App.tsx                  # Componente principal
│   └── main.tsx                 # Entry point
├── docs/                        # Documentação do projeto
│   ├── arquitetura/            # Especificações técnicas
│   ├── 02-trilha-estudo.md     # Ordem pedagógica
│   └── 02-matriz-cobertura.md  # Prioridades
└── README.md
```

## 🎓 Diretrizes para Implementação de Conteúdo

### Para cada módulo, seguir:

1. **Ler documentação**: 
   - `docs/02-trilha-estudo.md` - Ordem e pré-requisitos
   - `docs/arquitetura/01-requisitos.md` - Requisitos funcionais
   - `docs/arquitetura/05-motores.md` - Motor de questões

2. **Criar componente do módulo**:
   ```typescript
   src/modules/[CODIGO]/
   ├── Explanation.tsx      // Explicação curta
   ├── Activity.tsx         // Laboratório/atividade
   ├── Questions.tsx        // Questões por etapas
   └── questions.json       // Dados das questões
   ```

3. **Questões por etapas**:
   - 4 alternativas calculadas (não aleatórias)
   - Feedback específico por distrator
   - Fórmulas explícitas quando aplicável
   - Unidades corretas nos resultados

4. **Laboratórios virtuais**:
   - Apenas quando especificado no `activityType`
   - Começar simples, evoluir incrementalmente
   - Validação por regras, não valores arbitrários

5. **Validação técnica**:
   - Conferir livros de apoio listados
   - Verificar normas quando aplicável
   - Marcar conteúdo pendente com [VERIFICAR]

## 🔧 Tecnologias Utilizadas

- **React 18** - Framework UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool moderna
- **CSS3** - Estilização (sem framework CSS por enquanto)

## 📊 Sistema de Progresso

- Salvo automaticamente no `localStorage`
- Rastreamento por módulo:
  - Status (bloqueado/disponível/em progresso/concluído)
  - Questões completadas e corretas
  - Tentativas e dicas usadas
  - Data de início e conclusão

## 🎯 Próximos Passos

### Fase atual: Estrutura base completa ✅

### Próxima fase: Implementação incremental

**Ordem recomendada para implementação:**

1. **S01** - Desenergização (Primeiro módulo, sem pré-requisitos)
2. **F01** - Fundamentos (Base para muitos outros)
3. **M01** - Multímetro (Prático e importante)
4. **F02** - Lei de Ohm (Fundamental)
5. Continuar seguindo a trilha...

**Para cada módulo:**
- Implementar conteúdo pedagógico
- Revisar com usuário
- Ajustar conforme feedback
- Só então passar para o próximo

## 📝 Observações Importantes

### Baseado em:
- Análise de 241 questões de provas reais
- 35 subtemas identificados
- 206 grupos conservadores deduplica dos
- Priorização por matriz de cobertura
- Planos de curso oficiais CE e RR

### Limitações atuais:
- Matriz de Referência integral não confirmada
- Conteúdo pedagógico aguardando implementação
- Laboratórios virtuais complexos em desenvolvimento
- Questões são metas de produção, não conteúdo pronto

### Não fazer:
- ❌ Copiar questões reais das provas
- ❌ Inventar valores numéricos arbitrários
- ❌ Pular a ordem dos pré-requisitos
- ❌ Implementar sem revisar a arquitetura

## 🤝 Contribuindo

Este projeto segue um processo rigoroso de desenvolvimento incremental:

1. Ler toda documentação em `docs/`
2. Seguir arquitetura em `docs/arquitetura/`
3. Implementar um módulo por vez
4. Revisar antes de ampliar
5. Testar em dispositivos reais

## 📄 Licença

Projeto educacional - SAEP/SENAI

## 👥 Contato

Para dúvidas sobre implementação, consultar:
- Documentação em `docs/`
- Arquitetura em `docs/arquitetura/`
- Trilha em `docs/02-trilha-estudo.md`

---

**Última atualização:** 06/10/2026  
**Versão:** 1.0.0 - Estrutura Base  
**Status:** ✅ Pronto para implementação incremental de conteúdo
