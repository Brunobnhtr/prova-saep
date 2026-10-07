# Abrir a prévia

Na raiz do workspace:

```powershell
cd plataforma-saep
npm install
npm run dev
```

Abra http://127.0.0.1:5174/. A raiz do workspace contém a prévia separada de motores em 5173. Use Ctrl+F5 após mudanças. Se dependências foram atualizadas e houver tela em branco por cache do Vite, reinicie o servidor da plataforma com `npm run dev -- --force`.

Você verá 35 planos de temas, busca, filtros e temas salvos. S01 e F01 não têm pré-requisitos. Todos os conteúdos estão em preparação: não há aula completa, questões ou conclusão disponível. Clique em um tema para consultar o plano; salve para encontrar depois. Salvar não conta como aprendizagem.

Verificação: `npm test`, `npm run build`, `npm run lint`. Relatório: `../docs/08-auditoria-plataforma-2026-10-06.md`.
