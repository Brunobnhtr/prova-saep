// Dados dos 35 módulos na ordem da trilha de estudos
// Baseado em docs/02-trilha-estudo.md e docs/02-matriz-cobertura.md

import type { Module } from '../types';

export const MODULES: Module[] = [
  // MÓDULO 1: SEGURANÇA - S01
  {
    id: 'S01',
    order: 1,
    code: 'S01',
    area: 'Segurança',
    theme: 'Segurança em eletricidade',
    subtitle: 'Desenergização e reenergização',
    prerequisites: [],
    difficulty: 1,
    priority: 10,
    targetQuestions: 18,
    activityType: 'sequência normativa e cenário de decisão',
    supportBooks: ['livro-076 Segurança em Eletricidade'],
    contentStatus: 'planned'
  },

  // MÓDULO 2: SEGURANÇA - S02
  {
    id: 'S02',
    order: 2,
    code: 'S02',
    area: 'Segurança',
    theme: 'Segurança em eletricidade',
    subtitle: 'Qualificação, EPI, altura e zonas de risco',
    prerequisites: ['S01'],
    difficulty: 1,
    priority: 7,
    targetQuestions: 16,
    activityType: 'norma e análise de cenário',
    supportBooks: ['livro-075 Qualidade, Saúde, Meio Ambiente e Segurança', 'livro-076 Segurança em Eletricidade'],
    contentStatus: 'planned'
  },

  // MÓDULO 3: FUNDAMENTOS - F01
  {
    id: 'F01',
    order: 3,
    code: 'F01',
    area: 'Fundamentos',
    theme: 'Circuitos CC/CA',
    subtitle: 'Unidades e grandezas CC/CA',
    prerequisites: [],
    difficulty: 1,
    priority: 5,
    targetQuestions: 14,
    activityType: 'explicação e cálculo',
    supportBooks: ['livro-013 Eletricidade - Volume 1', 'livro-015 Eletricidade - Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 4: MEDIÇÕES - M01
  {
    id: 'M01',
    order: 4,
    code: 'M01',
    area: 'Medições',
    theme: 'Instrumentos',
    subtitle: 'Multímetro, alicate e seleção de escala',
    prerequisites: ['F01'],
    difficulty: 1,
    priority: 16,
    targetQuestions: 24,
    activityType: 'instrumento virtual e diagnóstico',
    supportBooks: ['livro-013 Eletricidade - Volume 1', 'livro-015 Eletricidade - Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 5: FUNDAMENTOS - F02
  {
    id: 'F02',
    order: 5,
    code: 'F02',
    area: 'Fundamentos',
    theme: 'Circuitos CC/CA',
    subtitle: 'Lei de Ohm e associação de resistores',
    prerequisites: ['F01'],
    difficulty: 2,
    priority: 11,
    targetQuestions: 14,
    activityType: 'cálculo passo a passo e circuito virtual',
    supportBooks: ['livro-013 Eletricidade - Volume 1'],
    contentStatus: 'planned'
  },

  // MÓDULO 6: FUNDAMENTOS - F03
  {
    id: 'F03',
    order: 6,
    code: 'F03',
    area: 'Fundamentos',
    theme: 'Circuitos CC/CA',
    subtitle: 'Frequência, formas de onda e reatância',
    prerequisites: ['F01', 'F02'],
    difficulty: 2,
    priority: 4,
    targetQuestions: 8,
    activityType: 'laboratório de formas de onda e cálculo',
    supportBooks: ['livro-015 Eletricidade - Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 7: FUNDAMENTOS - F04
  {
    id: 'F04',
    order: 7,
    code: 'F04',
    area: 'Fundamentos',
    theme: 'Energia e eficiência',
    subtitle: 'Potência, energia e fator de potência',
    prerequisites: ['F01', 'F02', 'F03'],
    difficulty: 2,
    priority: 8,
    targetQuestions: 14,
    activityType: 'cálculo e painel de cargas',
    supportBooks: ['livro-011 Eficiência Energética', 'livro-015 Eletricidade - Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 8: INSTALAÇÕES - I03
  {
    id: 'I03',
    order: 8,
    code: 'I03',
    area: 'Instalações',
    theme: 'Projetos elétricos',
    subtitle: 'Simbologia, unifilar, multifilar e CAD',
    prerequisites: ['F01'],
    difficulty: 2,
    priority: 17,
    targetQuestions: 18,
    activityType: 'leitura de planta e desenho',
    supportBooks: ['livro-049 Leitura e Interpretação de Desenho', 'livro-072 Projetos Elétricos Prediais - Volume 1'],
    contentStatus: 'planned'
  },

  // MÓDULO 9: REDES - R01
  {
    id: 'R01',
    order: 9,
    code: 'R01',
    area: 'Potência',
    theme: 'Redes de distribuição',
    subtitle: 'Estruturas, postes, alimentadores e topologias',
    prerequisites: ['I03', 'S02'],
    difficulty: 2,
    priority: 20,
    targetQuestions: 22,
    activityType: 'leitura de estruturas e projeto',
    supportBooks: ['livro-032 Fundamentos de Redes de Distribuição', 'livro-062 Montagem e Instalação de Redes'],
    contentStatus: 'planned'
  },

  // MÓDULO 10: PNEUMÁTICA - H01
  {
    id: 'H01',
    order: 10,
    code: 'H01',
    area: 'Automação',
    theme: 'Pneumática e hidráulica',
    subtitle: 'Válvulas, atuadores e simbologia',
    prerequisites: ['I03'],
    difficulty: 2,
    priority: 12,
    targetQuestions: 18,
    activityType: 'identificação de componentes',
    supportBooks: ['livro-001 Acionamento de Dispositivos Atuadores - Volume 1', 'livro-003 Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 11: AUTOMAÇÃO - A01
  {
    id: 'A01',
    order: 11,
    code: 'A01',
    area: 'Automação',
    theme: 'CLP e lógica',
    subtitle: 'Booleanos, binário, tabela verdade e Ladder',
    prerequisites: ['F01'],
    difficulty: 2,
    priority: 11,
    targetQuestions: 16,
    activityType: 'lógica interativa',
    supportBooks: ['livro-021 Eletrônica Digital', 'livro-031 Fundamentos de Automação'],
    contentStatus: 'planned'
  },

  // MÓDULO 12: MOTORES - E01
  {
    id: 'E01',
    order: 12,
    code: 'E01',
    area: 'Máquinas',
    theme: 'Motores elétricos',
    subtitle: 'Placa, potência, corrente e velocidade',
    prerequisites: ['F04', 'M01'],
    difficulty: 2,
    priority: 8,
    targetQuestions: 12,
    activityType: 'placa interativa e cálculo',
    supportBooks: ['livro-006 Acionamentos Eletroeletrônicos', 'livro-007 Comandos Elétricos'],
    contentStatus: 'planned'
  },

  // MÓDULO 13: TRANSFORMADORES - T01
  {
    id: 'T01',
    order: 13,
    code: 'T01',
    area: 'Máquinas',
    theme: 'Transformadores',
    subtitle: 'Relação de transformação e proteções',
    prerequisites: ['F03', 'F04'],
    difficulty: 2,
    priority: 8,
    targetQuestions: 12,
    activityType: 'cálculo e diagrama',
    supportBooks: ['livro-037 Instalações de SEP', 'livro-015 Eletricidade - Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 14: MEDIÇÃO SEP - T02
  {
    id: 'T02',
    order: 14,
    code: 'T02',
    area: 'Potência',
    theme: 'Medição e proteção em SEP',
    subtitle: 'TC, TP, relés e medição indireta',
    prerequisites: ['T01', 'M01', 'S01'],
    difficulty: 2,
    priority: 8,
    targetQuestions: 12,
    activityType: 'diagrama e cálculo',
    supportBooks: ['livro-037 Instalações de SEP', 'livro-070 Projetos de SEP'],
    contentStatus: 'planned'
  },

  // MÓDULO 15: SUBESTAÇÕES - R02
  {
    id: 'R02',
    order: 15,
    code: 'R02',
    area: 'Potência',
    theme: 'Subestações',
    subtitle: 'Equipamentos, barramentos e operação',
    prerequisites: ['R01', 'T02'],
    difficulty: 3,
    priority: 25,
    targetQuestions: 22,
    activityType: 'diagrama unifilar e cenário',
    supportBooks: ['livro-037 Instalações de SEP', 'livro-059 Manutenções de SEP', 'livro-070 Projetos de SEP'],
    contentStatus: 'planned'
  },

  // MÓDULO 16: INSTALAÇÕES PREDIAIS - I01
  {
    id: 'I01',
    order: 16,
    code: 'I01',
    area: 'Instalações',
    theme: 'Instalações prediais',
    subtitle: 'Tomadas, iluminação e previsão de cargas',
    prerequisites: ['F04', 'S01'],
    difficulty: 1,
    priority: 7,
    targetQuestions: 14,
    activityType: 'planta interativa e cálculo',
    supportBooks: ['livro-044 Instalações Elétricas Prediais - Volume 1', 'livro-045 Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 17: PROTEÇÃO - P01 (PRIORIDADE MÁXIMA)
  {
    id: 'P01',
    order: 17,
    code: 'P01',
    area: 'Proteção',
    theme: 'Dimensionamento',
    subtitle: 'Condutores, instalação e fatores de correção',
    prerequisites: ['F04', 'I01', 'S01'],
    difficulty: 3,
    priority: 36,
    targetQuestions: 24,
    activityType: 'cálculo com tabela e comparação',
    supportBooks: ['livro-045 Instalações Prediais - Volume 2', 'livro-071 Projetos Industriais'],
    contentStatus: 'planned'
  },

  // MÓDULO 18: PROTEÇÃO - P02
  {
    id: 'P02',
    order: 18,
    code: 'P02',
    area: 'Proteção',
    theme: 'Dimensionamento',
    subtitle: 'Disjuntores, fusíveis, curvas e curto-circuito',
    prerequisites: ['P01'],
    difficulty: 3,
    priority: 21,
    targetQuestions: 20,
    activityType: 'cálculo e leitura de curvas',
    supportBooks: ['livro-042 Instalações Industriais - Volume 1', 'livro-043 Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 19: INTERRUPTORES - I02
  {
    id: 'I02',
    order: 19,
    code: 'I02',
    area: 'Instalações',
    theme: 'Instalações prediais',
    subtitle: 'Interruptores, sensores e relé fotocélula',
    prerequisites: ['I01', 'M01'],
    difficulty: 2,
    priority: 12,
    targetQuestions: 18,
    activityType: 'ligação em diagrama e diagnóstico',
    supportBooks: ['livro-044 Instalações Prediais - Volume 1', 'livro-034 Instalação de Sensores'],
    contentStatus: 'planned'
  },

  // MÓDULO 20: PROTEÇÃO DR - P03
  {
    id: 'P03',
    order: 20,
    code: 'P03',
    area: 'Proteção',
    theme: 'Proteção de pessoas',
    subtitle: 'DR, IDR, DDR e coordenação de funções',
    prerequisites: ['S01', 'I01'],
    difficulty: 1,
    priority: 7,
    targetQuestions: 14,
    activityType: 'comparação de dispositivos e circuito',
    supportBooks: ['livro-044 Instalações Prediais - Volume 1', 'livro-076 Segurança em Eletricidade'],
    contentStatus: 'planned'
  },

  // MÓDULO 21: MEDIÇÕES - M02
  {
    id: 'M02',
    order: 21,
    code: 'M02',
    area: 'Medições',
    theme: 'Instrumentos',
    subtitle: 'Continuidade e resistência de isolamento',
    prerequisites: ['M01', 'S01'],
    difficulty: 1,
    priority: 6,
    targetQuestions: 16,
    activityType: 'multímetro e megômetro virtuais',
    supportBooks: ['livro-007 Comandos Elétricos', 'livro-058 Manutenção Elétrica'],
    contentStatus: 'planned'
  },

  // MÓDULO 22: SEGURANÇA - S03
  {
    id: 'S03',
    order: 22,
    code: 'S03',
    area: 'Segurança',
    theme: 'Segurança em eletricidade',
    subtitle: 'Classificação de tensão e documentação',
    prerequisites: ['F01', 'S01'],
    difficulty: 2,
    priority: 6,
    targetQuestions: 12,
    activityType: 'norma e leitura de prontuário',
    supportBooks: ['livro-076 Segurança em Eletricidade'],
    contentStatus: 'planned'
  },

  // MÓDULO 23: ENERGIA SOLAR - V01
  {
    id: 'V01',
    order: 23,
    code: 'V01',
    area: 'Energia',
    theme: 'Energia solar fotovoltaica',
    subtitle: 'Arranjos, potência e eficiência',
    prerequisites: ['F04', 'P01'],
    difficulty: 2,
    priority: 6,
    targetQuestions: 10,
    activityType: 'cálculo e arranjo virtual',
    supportBooks: ['livro-011 Eficiência Energética', 'livro-070 Projetos de SEP'],
    contentStatus: 'planned'
  },

  // MÓDULO 24: MANUTENÇÃO - D01
  {
    id: 'D01',
    order: 24,
    code: 'D01',
    area: 'Manutenção',
    theme: 'Manutenção e diagnóstico',
    subtitle: 'Preventiva, preditiva, corretiva e inspeções',
    prerequisites: ['S01'],
    difficulty: 1,
    priority: 4,
    targetQuestions: 12,
    activityType: 'classificação de cenários e planejamento',
    supportBooks: ['livro-055 Manutenção de Sistemas Industriais', 'livro-058 Manutenção Elétrica'],
    contentStatus: 'planned'
  },

  // MÓDULO 25: MANUTENÇÃO - D02
  {
    id: 'D02',
    order: 25,
    code: 'D02',
    area: 'Manutenção',
    theme: 'Manutenção e diagnóstico',
    subtitle: 'Termografia, conexões e localização de falhas',
    prerequisites: ['D01', 'M02'],
    difficulty: 1,
    priority: 7,
    targetQuestions: 16,
    activityType: 'diagnóstico visual',
    supportBooks: ['livro-055 Manutenção de Sistemas Industriais', 'livro-058 Manutenção Elétrica'],
    contentStatus: 'planned'
  },

  // MÓDULO 26: MOTORES - E02
  {
    id: 'E02',
    order: 26,
    code: 'E02',
    area: 'Máquinas',
    theme: 'Motores elétricos',
    subtitle: 'Bobinas, fechamentos e ligação monofásica/trifásica',
    prerequisites: ['E01', 'M02'],
    difficulty: 2,
    priority: 3,
    targetQuestions: 8,
    activityType: 'laboratório de terminais',
    supportBooks: ['livro-006 Acionamentos Eletroeletrônicos', 'livro-007 Comandos Elétricos'],
    contentStatus: 'planned'
  },

  // MÓDULO 27: COMANDOS - E03
  {
    id: 'E03',
    order: 27,
    code: 'E03',
    area: 'Máquinas',
    theme: 'Comandos e partidas',
    subtitle: 'Direta, reversão, selo e intertravamento',
    prerequisites: ['E02', 'P02'],
    difficulty: 2,
    priority: 9,
    targetQuestions: 14,
    activityType: 'diagrama de força e comando',
    supportBooks: ['livro-007 Comandos Elétricos', 'livro-060 Montagem de Sistemas de Controle'],
    contentStatus: 'planned'
  },

  // MÓDULO 28: PNEUMÁTICA - H02 (ALTA PRIORIDADE)
  {
    id: 'H02',
    order: 28,
    code: 'H02',
    area: 'Automação',
    theme: 'Pneumática e hidráulica',
    subtitle: 'Sequências, selo e diagnóstico eletropneumático',
    prerequisites: ['H01', 'E03', 'A01'],
    difficulty: 3,
    priority: 26,
    targetQuestions: 22,
    activityType: 'laboratório de sequência',
    supportBooks: ['livro-001 Acionamento Volume 1', 'livro-003 Volume 2'],
    contentStatus: 'planned'
  },

  // MÓDULO 29: AUTOMAÇÃO - A02 (ALTA PRIORIDADE)
  {
    id: 'A02',
    order: 29,
    code: 'A02',
    area: 'Automação',
    theme: 'CLP e lógica',
    subtitle: 'Entradas, saídas e controle sequencial',
    prerequisites: ['A01', 'E03'],
    difficulty: 3,
    priority: 24,
    targetQuestions: 20,
    activityType: 'laboratório de CLP',
    supportBooks: ['livro-031 Fundamentos de Automação', 'livro-005 Acionamento de Dispositivos'],
    contentStatus: 'planned'
  },

  // MÓDULO 30: INVERSORES - E06 (ALTA PRIORIDADE)
  {
    id: 'E06',
    order: 30,
    code: 'E06',
    area: 'Máquinas',
    theme: 'Acionamentos',
    subtitle: 'Inversor, soft-starter e parametrização',
    prerequisites: ['E03', 'F03'],
    difficulty: 3,
    priority: 23,
    targetQuestions: 20,
    activityType: 'painel virtual e diagnóstico',
    supportBooks: ['livro-006 Acionamentos Eletroeletrônicos'],
    contentStatus: 'planned'
  },

  // MÓDULO 31: PARTIDAS - E04
  {
    id: 'E04',
    order: 31,
    code: 'E04',
    area: 'Máquinas',
    theme: 'Comandos e partidas',
    subtitle: 'Estrela-triângulo e compensadora',
    prerequisites: ['E03'],
    difficulty: 3,
    priority: 12,
    targetQuestions: 12,
    activityType: 'laboratório e escolha de componentes',
    supportBooks: ['livro-007 Comandos Elétricos', 'livro-006 Acionamentos'],
    contentStatus: 'planned'
  },

  // MÓDULO 32: SENSORES - A03
  {
    id: 'A03',
    order: 32,
    code: 'A03',
    area: 'Automação',
    theme: 'Sensores',
    subtitle: 'Sensores de presença, alarme e nível',
    prerequisites: ['A02', 'I02'],
    difficulty: 1,
    priority: 4,
    targetQuestions: 12,
    activityType: 'seleção e diagrama',
    supportBooks: ['livro-034 Instalação de Sensores', 'livro-047 Integração de Sensores'],
    contentStatus: 'planned'
  },

  // MÓDULO 33: DAHLANDER - E05
  {
    id: 'E05',
    order: 33,
    code: 'E05',
    area: 'Máquinas',
    theme: 'Comandos e partidas',
    subtitle: 'Dahlander e duas velocidades',
    prerequisites: ['E03'],
    difficulty: 3,
    priority: 3,
    targetQuestions: 8,
    activityType: 'diagrama e comparação de velocidades',
    supportBooks: ['livro-007 Comandos Elétricos', 'livro-006 Acionamentos'],
    contentStatus: 'planned'
  },

  // MÓDULO 34: ATERRAMENTO - P04
  {
    id: 'P04',
    order: 34,
    code: 'P04',
    area: 'Proteção',
    theme: 'Aterramento e SPDA',
    subtitle: 'Esquemas de aterramento e equipotencialização',
    prerequisites: ['S01', 'I03'],
    difficulty: 1,
    priority: 3,
    targetQuestions: 10,
    activityType: 'diagrama interativo',
    supportBooks: ['livro-044 Instalações Prediais - Volume 1', 'livro-076 Segurança'],
    contentStatus: 'planned'
  },

  // MÓDULO 35: SPDA - P05
  {
    id: 'P05',
    order: 35,
    code: 'P05',
    area: 'Proteção',
    theme: 'Aterramento e SPDA',
    subtitle: 'Captação, descida, aterramento e DPS',
    prerequisites: ['P04'],
    difficulty: 1,
    priority: 10,
    targetQuestions: 20,
    activityType: 'identificação de subsistemas e norma',
    supportBooks: ['livro-045 Instalações Prediais - Volume 2', 'livro-076 Segurança'],
    contentStatus: 'planned'
  }
];

// Função auxiliar para obter módulo por ID
export function getModuleById(id: string): Module | undefined {
  return MODULES.find(m => m.id === id);
}

// Função para verificar se módulo está desbloqueado
export function isModuleUnlocked(moduleId: string, completedModules: string[]): boolean {
  const module = getModuleById(moduleId);
  if (!module) return false;
  
  // Se não tem pré-requisitos, está desbloqueado
  if (module.prerequisites.length === 0) return true;
  
  // Verifica se todos os pré-requisitos foram completados
  return module.prerequisites.every(prereq => completedModules.includes(prereq));
}

// Função para obter próximos módulos disponíveis
export function getAvailableModules(completedModules: string[]): Module[] {
  return MODULES.filter(module => 
    !completedModules.includes(module.id) &&
    isModuleUnlocked(module.id, completedModules)
  );
}
