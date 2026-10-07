// Tipos base do sistema SAEP
// Baseado em docs/arquitetura/04-modelo-dados.md

export type DifficultyLevel = 1 | 2 | 3;

export type ModuleStatus = 'locked' | 'available' | 'in_progress' | 'completed';

export type QuestionType = 'calculation' | 'conceptual' | 'diagram' | 'procedure';

export interface Module {
  id: string;
  order: number;
  code: string; // Ex: S01, F01, M01...
  area: string;
  theme: string;
  subtitle: string;
  prerequisites: string[]; // IDs dos módulos pré-requisitos
  difficulty: DifficultyLevel;
  priority: number; // F × D da matriz
  targetQuestions: number; // Meta de questões
  activityType: string;
  supportBooks: string[];
  contentStatus: 'planned' | 'preview' | 'ready';
}

export interface Question {
  id: string;
  moduleId: string;
  type: QuestionType;
  version: string;
  seed?: number; // Para questões paramétricas
  statement: string;
  steps?: QuestionStep[]; // Questões por etapas
  options: QuestionOption[];
  correctAnswer: string;
  explanation: string;
  hints?: string[];
  difficulty: DifficultyLevel;
  tags: string[];
}

export interface QuestionStep {
  id: string;
  order: number;
  instruction: string;
  formula?: string;
  parameters?: Record<string, number>;
  options: QuestionOption[];
  correctAnswer: string;
  feedback: Record<string, string>; // feedback por alternativa
  hint?: string;
}

export interface QuestionOption {
  id: string;
  label: string; // A, B, C, D
  text: string;
  isCorrect: boolean;
}

export interface UserProgress {
  moduleId: string;
  status: ModuleStatus;
  startedAt?: string;
  completedAt?: string;
  score: number; // Pontuação geral
  questionsCompleted: number;
  questionsCorrect: number;
  attempts: number;
  hintsUsed: number;
  lastStudied?: string;
  reviewQueue: string[]; // IDs de questões para revisar
}

export interface QuestionAttempt {
  questionId: string;
  attemptNumber: number;
  answer: string;
  isCorrect: boolean;
  usedHint: boolean;
  timestamp: string;
  timeSpent: number; // segundos
}

export interface StudySession {
  id: string;
  moduleId: string;
  startTime: string;
  endTime?: string;
  questionsAttempted: QuestionAttempt[];
  completed: boolean;
}

// Sistema de revisão espaçada
export interface ReviewSchedule {
  questionId: string;
  nextReviewDate: string;
  interval: number; // dias
  easeFactor: number;
  repetitions: number;
  lastReviewed?: string;
}

// Mini-simulado
export interface MiniExam {
  id: string;
  title: string;
  modules: string[]; // IDs dos módulos cobertos
  questions: Question[];
  duration: number; // minutos
  startedAt?: string;
  submittedAt?: string;
  score?: number;
}

// Laboratório virtual (estrutura base)
export interface LabActivity {
  id: string;
  moduleId: string;
  title: string;
  description: string;
  type: 'simulation' | 'diagram' | 'calculation' | 'procedure';
  safetyChecklist?: string[]; // Para módulos de segurança
  components?: LabComponent[];
  validationRules?: ValidationRule[];
}

export interface LabComponent {
  id: string;
  type: string; // 'motor', 'multimeter', 'wire', 'breaker', etc
  position: { x: number; y: number };
  properties: Record<string, unknown>;
  connections: string[]; // IDs de outros componentes conectados
}

export interface ValidationRule {
  id: string;
  condition: string;
  message: string;
  severity: 'error' | 'warning' | 'info';
}

// Backup e exportação
export interface UserData {
  version: string;
  exportedAt: string;
  progress: UserProgress[];
  reviewSchedule: ReviewSchedule[];
  sessions: StudySession[];
  preferences: UserPreferences;
}

export interface UserPreferences {
  soundEnabled: boolean;
  darkMode: boolean;
  fontSize: 'small' | 'medium' | 'large';
  animationsEnabled: boolean;
  language: 'pt-BR';
}
