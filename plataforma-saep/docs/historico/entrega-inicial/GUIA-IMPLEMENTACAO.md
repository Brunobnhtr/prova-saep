# 📘 Guia de Implementação - Para a IA Mestre

## 🎯 Objetivo deste Documento

Este guia orienta a implementação incremental do conteúdo pedagógico nos 35 módulos da Plataforma SAEP, seguindo rigorosamente as diretrizes do projeto.

## ✅ O que JÁ está pronto

### Estrutura Base Completa

- ✅ Projeto React + TypeScript + Vite configurado
- ✅ 35 módulos mapeados em `src/data/modules.ts`
- ✅ Tipos TypeScript definidos em `src/types/index.ts`
- ✅ Componentes base criados:
  - `ModuleCatalog.tsx` - Catálogo com sistema de bloqueio
  - `ModuleDetail.tsx` - Tela de detalhes e estudo
  - `ProgressBar.tsx` - Barra de progresso global
- ✅ Sistema de progresso com localStorage
- ✅ Ordem pedagógica respeitada (pré-requisitos)
- ✅ CSS responsivo (Desktop + Mobile)
- ✅ Navegação funcional

### Arquitetura Definida

- Stack: React + TypeScript + Vite ✅
- Algoritmo: Grafo de ligações com regras ✅
- Fidelidade: Pedagógica intermediária ✅
- Offline: Preparado (service worker futuro)

## 🚧 O que PRECISA ser implementado

### Para CADA módulo (35 vezes):

1. **Explicação curta** (componente)
2. **Atividade/Laboratório** (específico do tema)
3. **Questões por etapas** (4 alternativas calculadas)
4. **Sistema de revisão** (espaçamento inteligente)

## 📋 REGRAS FUNDAMENTAIS

### ⚠️ SEMPRE SEGUIR

1. **Ordem cronológica**: Implementar na sequência da trilha (S01, S02, F01...)
2. **Um módulo por vez**: Implementar completamente antes do próximo
3. **Revisar com usuário**: Mostrar, ajustar, só então avançar
4. **Consultar docs/**: Toda decisão técnica está documentada
5. **Pré-requisitos**: Nunca pular a ordem pedagógica

### ❌ NUNCA FAZER

1. ❌ Copiar questões reais das provas (criar originais)
2. ❌ Inventar valores numéricos sem base técnica
3. ❌ Criar laboratórios complexos de uma vez (incremental)
4. ❌ Pular a validação com usuário
5. ❌ Implementar vários módulos em paralelo
6. ❌ Usar emojis excessivamente (só se usuário pedir)

## 🗺️ Roteiro de Implementação

### Fase 1: Módulos Básicos (1-7)

**Ordem de implementação sugerida:**

#### 1. **S01 - Desenergização e reenergização** (Começar aqui!)

**Por quê?**
- Sem pré-requisitos
- Tema de segurança (prioritário)
- 18 questões planejadas
- Atividade: sequência normativa

**O que implementar:**

```typescript
// src/modules/S01/
├── Explanation.tsx      // Conceitos de segurança
├── Activity.tsx         // Cenário de decisão
├── Questions.tsx        // Questões sobre procedimentos
└── data.json           // Questões e cenários
```

**Conteúdo (baseado em livro-076):**
- Etapas de desenergização (seccionamento, impedimento, constatação...)
- Zonas controladas
- Procedimentos de reenergização
- Cenários de decisão (qual procedimento aplicar?)

**Tipo de questões:**
- Sequência correta de etapas
- Identificação de riscos
- Escolha de EPI adequado
- Análise de cenários

#### 2. **F01 - Unidades e grandezas CC/CA**

**Por quê?**
- Sem pré-requisitos
- Base para muitos módulos
- 14 questões planejadas
- Atividade: explicação e cálculo

**O que implementar:**
- Conversões de unidades (V, A, W, Ω)
- Notação científica
- Múltiplos e submúltiplos
- Cálculos simples

**Tipo de questões (por etapas):**

Exemplo:
```
Etapa 1: Converter 5000 mA para A
A) 0,5 A
B) 5 A ✓
C) 50 A
D) 500 A

Feedback específico:
- A: "Você dividiu por 100, mas mA → A divide por 1000"
- B: "Correto! 5000 mA ÷ 1000 = 5 A"
- C: "Você multiplicou quando deveria dividir"
- D: "Revise a conversão mA → A"
```

#### 3. **S02 - EPI e zonas de risco**
**Pré-requisito:** S01 ✓

#### 4. **M01 - Multímetro**
**Pré-requisito:** F01 ✓
**Importante:** Instrumento virtual (já tem base na prévia-01)

#### 5-7: F02, F03, F04
**Fundamentos de circuitos**

### Fase 2: Módulos Intermediários (8-20)

- Instalações (I01, I02, I03)
- Proteção (P01, P02, P03) - **ALTA PRIORIDADE**
- Redes (R01, R02)
- Manutenção (D01, D02)

### Fase 3: Módulos Avançados (21-35)

- Motores (E01-E06)
- Automação (A01-A03, H01-H02)
- Aterramento (P04, P05)

## 📐 Template de Implementação

### Estrutura de um Módulo Completo

```typescript
// src/modules/[CODIGO]/index.tsx
import { useState } from 'react';
import Explanation from './Explanation';
import Activity from './Activity';
import Questions from './Questions';
import Review from './Review';

interface ModuleContentProps {
  onComplete: (score: number) => void;
}

export default function ModuleContent({ onComplete }: ModuleContentProps) {
  const [step, setStep] = useState<'explanation' | 'activity' | 'questions' | 'review'>('explanation');
  const [activityCompleted, setActivityCompleted] = useState(false);
  const [questionsScore, setQuestionsScore] = useState(0);

  return (
    <div className="module-content">
      {step === 'explanation' && (
        <Explanation onNext={() => setStep('activity')} />
      )}
      
      {step === 'activity' && (
        <Activity 
          onComplete={() => {
            setActivityCompleted(true);
            setStep('questions');
          }} 
        />
      )}
      
      {step === 'questions' && (
        <Questions 
          onComplete={(score) => {
            setQuestionsScore(score);
            setStep('review');
          }}
        />
      )}
      
      {step === 'review' && (
        <Review 
          score={questionsScore}
          onFinish={() => onComplete(questionsScore)}
        />
      )}
    </div>
  );
}
```

### Componente de Questões por Etapas

```typescript
// src/modules/[CODIGO]/Questions.tsx
import { useState } from 'react';
import { QuestionStep } from '../../types';

interface QuestionsProps {
  onComplete: (score: number) => void;
}

export default function Questions({ onComplete }: QuestionsProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [hintsUsed, setHintsUsed] = useState(0);

  // Carregar questões do data.json
  const steps: QuestionStep[] = [];

  const handleSubmit = () => {
    setShowFeedback(true);
    // Lógica de feedback e próxima etapa
  };

  return (
    <div className="questions-container">
      <div className="question-header">
        <span>Etapa {currentStep + 1} de {steps.length}</span>
      </div>
      
      {/* Instrução da etapa */}
      <div className="question-instruction">
        <h3>{steps[currentStep]?.instruction}</h3>
        {steps[currentStep]?.formula && (
          <div className="formula">{steps[currentStep].formula}</div>
        )}
      </div>
      
      {/* Alternativas */}
      <div className="options">
        {steps[currentStep]?.options.map((option) => (
          <button
            key={option.id}
            className={`option ${selectedAnswer === option.id ? 'selected' : ''}`}
            onClick={() => setSelectedAnswer(option.id)}
            disabled={showFeedback}
          >
            {option.label}) {option.text}
          </button>
        ))}
      </div>
      
      {/* Botões de ação */}
      <div className="actions">
        {!showFeedback && (
          <>
            <button onClick={handleSubmit} disabled={!selectedAnswer}>
              Verificar Resposta
            </button>
            <button onClick={() => setHintsUsed(h => h + 1)}>
              💡 Dica
            </button>
          </>
        )}
      </div>
      
      {/* Feedback */}
      {showFeedback && (
        <div className={`feedback ${selectedAnswer === steps[currentStep].correctAnswer ? 'correct' : 'incorrect'}`}>
          {steps[currentStep].feedback[selectedAnswer || '']}
        </div>
      )}
    </div>
  );
}
```

## 📊 Estrutura de Dados (JSON)

```json
// src/modules/S01/data.json
{
  "moduleId": "S01",
  "explanation": {
    "title": "Desenergização e Reenergização",
    "sections": [
      {
        "subtitle": "Por que é importante?",
        "content": "A desenergização adequada salva vidas..."
      }
    ],
    "keyPoints": [
      "Seccionamento",
      "Impedimento",
      "Constatação",
      "Proteção",
      "Aterramento",
      "Equipotencialização"
    ]
  },
  "activity": {
    "type": "scenario",
    "title": "Cenário: Manutenção em Painel",
    "description": "Você precisa realizar manutenção...",
    "steps": [
      {
        "id": 1,
        "action": "Escolha a primeira etapa",
        "options": [
          { "id": "a", "text": "Abrir o painel", "correct": false },
          { "id": "b", "text": "Seccionar a alimentação", "correct": true }
        ]
      }
    ]
  },
  "questions": [
    {
      "id": "S01-Q01",
      "type": "conceptual",
      "steps": [
        {
          "id": 1,
          "instruction": "Qual a PRIMEIRA etapa da desenergização?",
          "options": [
            { "id": "a", "label": "A", "text": "Constatar ausência de tensão", "correct": false },
            { "id": "b", "label": "B", "text": "Seccionar", "correct": true },
            { "id": "c", "label": "C", "text": "Aterrar", "correct": false },
            { "id": "d", "label": "D", "text": "Sinalizar", "correct": false }
          ],
          "correctAnswer": "b",
          "feedback": {
            "a": "A constatação vem DEPOIS do seccionamento. Primeiro precisamos garantir que a energia está cortada.",
            "b": "Correto! O seccionamento é sempre a primeira etapa para isolar a fonte de energia.",
            "c": "O aterramento é importante, mas vem depois de seccionar e constatar.",
            "d": "A sinalização é importante durante todo o processo, mas não é a primeira etapa técnica."
          },
          "hint": "Pense: qual ação garante que a energia não chegará ao local de trabalho?"
        }
      ]
    }
  ]
}
```

## 🎨 Diretrizes de UI/UX

### Cores por Tipo

- **Sucesso** (correto): `#28a745`
- **Erro** (incorreto): `#dc3545`
- **Aviso** (dica): `#ffc107`
- **Info** (neutro): `#17a2b8`

### Feedback Visual

```css
.option.correct {
  border-color: #28a745;
  background: #d4edda;
}

.option.incorrect {
  border-color: #dc3545;
  background: #f8d7da;
}
```

### Acessibilidade

- Sempre incluir `aria-label` em botões com ícones
- Navegação por teclado funcional
- Contraste WCAG AA mínimo
- Feedback não depende só de cor

## 📚 Documentos de Referência

### Obrigatórios para cada módulo:

1. **docs/02-trilha-estudo.md** - Ordem e pré-requisitos
2. **docs/02-matriz-cobertura.md** - Prioridades
3. **docs/arquitetura/01-requisitos.md** - Requisitos funcionais
4. **docs/arquitetura/05-motores.md** - Motor de questões
5. **src/data/modules.ts** - Configuração do módulo

### Livros de apoio:

Listados em cada módulo em `supportBooks`

## ✅ Checklist de Implementação

### Para cada módulo:

- [ ] Ler documentação do módulo
- [ ] Verificar pré-requisitos implementados
- [ ] Criar estrutura de pastas
- [ ] Implementar Explanation.tsx
- [ ] Implementar Activity.tsx (específico)
- [ ] Criar data.json com questões
- [ ] Implementar Questions.tsx
- [ ] Criar pelo menos 8 questões originais
- [ ] Testar todas as alternativas
- [ ] Verificar feedback de cada distrator
- [ ] Testar navegação completa
- [ ] Revisar com usuário
- [ ] Ajustar conforme feedback
- [ ] Marcar como concluído
- [ ] Partir para próximo módulo

## 🚀 Começando Agora

### Primeiro passo:

```bash
# Entre no projeto
cd plataforma-saep

# Execute em dev
npm run dev

# Crie a pasta do primeiro módulo
mkdir -p src/modules/S01

# Comece pelo S01!
```

### Modelo inicial S01:

```typescript
// src/modules/S01/index.tsx
export { default } from './ModuleContent';
```

## 💬 Comunicação com Usuário

Após implementar cada módulo:

1. **Mostrar** o que foi feito
2. **Explicar** as escolhas técnicas
3. **Aguardar** feedback e ajustes
4. **Só então** partir para o próximo

## 🎯 Objetivo Final

35 módulos completos seguindo a trilha pedagógica, cada um com:
- Explicação clara
- Atividade prática
- Questões por etapas (4 alternativas)
- Feedback específico
- Sistema de revisão
- Progresso rastreado

---

**Boa implementação! 🚀**

*Lembre-se: Qualidade > Quantidade. Um módulo bem feito por vez.*
