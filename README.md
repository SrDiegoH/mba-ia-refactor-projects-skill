# Criação de Skills — Refatoração Arquitetural Automatizada

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Exemplo de Uso no CLI

```bash
# Executar a skill no projeto com problemas
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** uma das três opções abaixo (não são aceitas outras ferramentas):
  - Claude Code
  - Gemini CLI
  - OpenAI Codex
- **Recurso:** Custom Skills (ou o equivalente na ferramenta escolhida)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota sobre a ferramenta:** Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência, pois é a ferramenta utilizada no curso. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (SKILL.md + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia — lidando tanto com código completamente desestruturado quanto com projetos que já possuem alguma separação de camadas.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

**Tarefas:**

Criar a skill dentro do projeto `code-smells-project/` e implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar arquivos de referência em Markdown que forneçam à skill o conhecimento necessário para executar as 3 fases. Os arquivos devem cobrir **obrigatoriamente** as seguintes áreas de conhecimento:

| Área de conhecimento | O que deve conter |
|---|---|
| Análise de projeto | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura |
| Catálogo de anti-patterns | Anti-patterns com sinais de detecção e classificação de severidade |
| Template de relatório | Formato padronizado do relatório de auditoria (Fase 2) |
| Guidelines de arquitetura | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| Playbook de refatoração | Padrões concretos de transformação para cada anti-pattern (com exemplos de código) |

> **Nota:** Você tem liberdade para organizar os arquivos de referência como preferir — pode usar os nomes e a quantidade de arquivos que fizer sentido para sua skill. O importante é que todas as 5 áreas de conhecimento estejam cobertas. O nome da skill (`refactor-arch`) e o arquivo `SKILL.md` são obrigatórios e não devem ser alterados. O path da skill segue a convenção da ferramenta escolhida (no Claude Code, por exemplo, é `.claude/skills/refactor-arch/`).

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos, independente da stack ou nível de organização
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

Execute sua skill nos 3 projetos e valide que ela funciona em todas as stacks.

#### Projeto 1 — code-smells-project (Python/Flask)

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

> **Nota:** O comando acima é o exemplo com Claude Code. Se você estiver usando Gemini CLI ou Codex, utilize o comando equivalente para invocar uma skill na sua ferramenta.

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 3 — task-manager-api (Python/Flask)

Agora o teste com um projeto Python/Flask que já possui alguma organização de camadas (models, routes, services, utils).

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente Python/Flask como stack e identifica o domínio de Task Manager
  - A Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (todos os endpoints devem continuar respondendo)
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado do projeto no repositório

> **Nota:** Este projeto já possui alguma separação de camadas, mas isso não significa que a arquitetura está adequada. A skill deve identificar tanto problemas de código (segurança, performance, qualidade) quanto oportunidades de melhoria arquitetural. Se houver mudanças estruturais necessárias, a skill deve propô-las e executá-las.

#### Validação

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

> **Dica:** Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

Faça um fork do repositório base contendo os três projetos com code smells.

> **Nota:** A estrutura abaixo usa Claude Code como exemplo (`.claude/skills/`). Se estiver usando outra ferramenta, adapte os caminhos conforme a convenção dela.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API de E-commerce)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (LMS API com checkout)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — Python/Flask (API de Task Manager)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + arquivos de referência)
- Código refatorado dos 3 projetos — resultado da execução da Fase 3, commitado no repositório
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API de E-commerce Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — LMS API Node.js/Express (com fluxo de checkout) e problemas de implementação
- `task-manager-api/` — API de Task Manager Python/Flask com organização parcial e problemas de segurança/qualidade

> **Dica:** Cada projeto contém problemas intencionais de diferentes severidades (CRITICAL, HIGH, MEDIUM, LOW), incluindo falhas de segurança, violações arquiteturais e problemas de qualidade de código. Parte do desafio é identificá-los por conta própria através da análise manual do código.

### README.md deve conter

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: como estruturou o SKILL.md e os arquivos de referência
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (a ferramenta escolhida — Claude Code, Gemini CLI ou Codex — instalada e configurada)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

### Ordem de execução sugerida

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os arquivos de referência.

**3. Executar nos 3 projetos**

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 de cada projeto em `reports/audit-project-{1,2,3}.md`.

**4. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério | Requisito |
|---|---|
| Fase 1 detecta stack corretamente | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** Este projeto já possui alguma organização. "aplicação funciona" significa que a API inicia sem erros e todos os endpoints continuam respondendo corretamente.

## Referências

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Documentação oficial sobre como criar e estruturar Skills
- [Claude Code: Overview](https://docs.anthropic.com/en/docs/claude-code/overview) — Visão geral do Claude Code e suas capacidades
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Guia completo da Anthropic sobre construção de Skills
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um projeto já parcialmente organizado não vai ter as mesmas transformações de um monolito. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
- **Consulte as referências do curso** — revise a documentação oficial da ferramenta escolhida e os materiais das aulas para relembrar a estrutura e anatomia de uma skill.

---
---

# Resultado final

## Análise Manual

### Projeto 1 — code-smells-project (Python/Flask E-commerce)

**Informações Gerais**

- Linguagem: Python
- Framework: Flask
- Banco de Dados: SQLite
- Arquitetura Atual: Monolítica
- Domínio: E-commerce

**Resumo**

O projeto concentra praticamente toda a lógica da aplicação em poucos arquivos (`app.py`, `controllers.py`, `models.py` e `database.py`), apresentando graves problemas de segurança, separação de responsabilidades e manutenção.

| Severidade | Finding | Arquivo | Justificativa |
|:----------:|---------|---------|---------------|
| CRITICAL | Credenciais Hardcoded | `app.py` | `SECRET_KEY` em código-fonte expõe sessões e credenciais diretamente no repositório |
| CRITICAL | Execução Arbitrária de SQL | `app.py` (POST /admin/query) | Executa qualquer SQL recebido do usuário — leitura, alteração ou exclusão total do banco |
| CRITICAL | SQL Injection | `models.py` | Consultas montadas por concatenação de strings permitem acesso indevido a qualquer dado |
| HIGH | Senhas em Texto Puro | `database.py`, `models.py` | Senhas armazenadas sem hash expõem todas as credenciais em caso de vazamento do banco |
| HIGH | Endpoint Administrativo Sem Autenticação | `app.py` (POST /admin/reset-db) | Qualquer usuário anônimo pode apagar todos os dados da aplicação |
| HIGH | God Class / God Module | `models.py` | Um único módulo concentra banco, autenticação, pedidos, usuários, produtos e relatórios — impossível testar em isolamento |
| MEDIUM | Regras de Negócio em Controllers | `controllers.py` | Validações e regras de domínio nas rotas dificultam reutilização e testes |
| MEDIUM | N+1 Queries | `models.py` | Consultas dentro de loops causam degradação de performance proporcional ao volume de dados |
| LOW | Logging com print() | Geral | `print()` não oferece níveis, formatação ou destino configurável |
| LOW | Strings Mágicas | Geral | Valores fixos repetidos aumentam custo de manutenção e risco de inconsistência |

**Resumo Final:** CRITICAL: 3 · HIGH: 3 · MEDIUM: 2 · LOW: 2 · **Total: 10 findings**

---

### Projeto 2 — ecommerce-api-legacy (Node.js/Express LMS)

**Informações Gerais**

- Linguagem: JavaScript
- Framework: Express
- Banco de Dados: SQLite (em memória)
- Arquitetura Atual: Monolítica
- Domínio: LMS / Plataforma de Cursos

**Resumo**

O projeto apresenta forte acoplamento dentro da classe `AppManager`, que mistura responsabilidades de pagamento, usuários, cursos, auditoria e persistência, além de problemas relevantes de segurança.

| Severidade | Finding | Arquivo | Justificativa |
|:----------:|---------|---------|---------------|
| CRITICAL | Credenciais Hardcoded | `utils.js` | Configurações sensíveis e chaves diretamente no código-fonte expõem segredos no repositório |
| CRITICAL | Criptografia Insegura | `utils.js`, `AppManager.js` | `badCrypto()` para senhas é reversível — qualquer acesso ao banco compromete todas as credenciais |
| HIGH | God Class | `AppManager.js` | A mesma classe gerencia usuários, cursos, matrículas, pagamentos, auditoria, banco e rotas — violação completa de SRP |
| HIGH | Lógica de Negócio Dentro das Rotas | `AppManager.js` | Checkout, matrícula e auditoria no handler HTTP — violação direta de MVC e SOLID |
| HIGH | Dados Sensíveis em Logs | `AppManager.js` | Cartões e informações de pagamento em `console.log` criam risco de vazamento em produção |
| MEDIUM | Banco em Memória | `AppManager.js` | `:memory:` causa perda total dos dados a cada reinicialização — inviável em produção |
| MEDIUM | Ausência de Camada de Serviços | Geral | Toda regra de negócio acoplada às rotas impossibilita reutilização e testes unitários |
| LOW | Convenções Inconsistentes | Geral | Nomes como `usr`, `eml`, `pwd`, `c_id` reduzem legibilidade e aumentam custo de manutenção |
| LOW | Logging Não Estruturado | Geral | `console.log` sem níveis dificulta monitoramento e rastreamento de erros em produção |

**Resumo Final:** CRITICAL: 2 · HIGH: 3 · MEDIUM: 2 · LOW: 2 · **Total: 9 findings**

---

### Projeto 3 — task-manager-api (Python/Flask Task Manager)

**Informações Gerais**

- Linguagem: Python
- Framework: Flask
- Banco de Dados: SQLAlchemy (SQLite)
- Arquitetura Atual: Parcialmente Organizada
- Domínio: Task Manager

**Resumo**

O projeto apresenta estrutura melhor que os demais (models/, routes/, services/), mas ainda há forte concentração de regras de negócio nas rotas e problemas de qualidade arquitetural relevantes.

| Severidade | Finding | Arquivo | Justificativa |
|:----------:|---------|---------|---------------|
| HIGH | Regras de Negócio nas Rotas | `routes/task_routes.py` | Validações, cálculos, verificações de status e regras de atraso nas rotas violam separação de responsabilidades |
| HIGH | N+1 Queries | `routes/task_routes.py` | Para cada task, consultas adicionais para usuário e categoria — degradação de performance proporcional ao volume |
| MEDIUM | Tratamento Genérico de Exceções | `routes/task_routes.py` | `except:` nulo oculta erros reais e dificulta diagnóstico e rastreamento de falhas |
| MEDIUM | Duplicação de Regras de Overdue | `routes/task_routes.py` | Lógica de overdue repetida em múltiplos endpoints viola DRY e cria risco de inconsistência |
| MEDIUM | Serialização Manual | `routes/task_routes.py` | Montagem manual de dicionários para resposta em todos os endpoints — código repetitivo e frágil |
| LOW | Imports Não Utilizados | `routes/task_routes.py` | Dependências desnecessárias aumentam acoplamento e ruído no código |
| LOW | Strings Mágicas | `routes/task_routes.py` | Status como `"pending"`, `"in_progress"`, `"done"`, `"cancelled"` espalhados tornam manutenção mais custosa |
| LOW | Validações Repetidas | `routes/task_routes.py` | Validações distribuídas em múltiplos endpoints duplicam lógica e criam pontos cegos |

**Resumo Final:** HIGH: 2 · MEDIUM: 3 · LOW: 3 · **Total: 8 findings**

> **Observação:** Este é o projeto mais próximo de uma arquitetura organizada. A refatoração necessária é significativamente menor que nos outros dois projetos — estratégia incremental em vez de reescrita.

## Construção da Skill

### Decisões de Design

A skill foi construída seguindo um fluxo em quatro fases:

1. Análise do projeto
2. Auditoria arquitetural
3. Refatoração
4. Validação

Essa divisão foi adotada para garantir que o projeto fosse compreendido antes de qualquer modificação.

Outra decisão importante foi manter o `SKILL.md` apenas como orquestrador do processo, enquanto as regras e conhecimentos específicos foram organizados em arquivos de referência separados. Isso facilita manutenção e reduz ambiguidades.

---

### Anti-Patterns Incluídos

Foram selecionados anti-patterns comuns em aplicações legadas e fáceis de identificar automaticamente:

* God Class
* God Method
* Hardcoded Credentials
* Business Logic in Routes
* Business Logic in Controllers
* Tight Coupling
* Global Mutable State
* Duplicated Logic
* Missing Validation
* Deprecated APIs

Esses problemas foram escolhidos por serem frequentes e por impactarem diretamente a organização MVC e a manutenibilidade do sistema.

---

### Como a Skill Foi Tornada Agnóstica de Tecnologia

A skill foi projetada com foco em conceitos arquiteturais, não em frameworks específicos.

As regras são baseadas em responsabilidades de:

* Rotas
* Controladores
* Modelos
* Fluxo de dependências

A detecção da stack foi isolada em documentos específicos, permitindo que a mesma lógica funcione em diferentes tecnologias.

Os exemplos utilizados contemplam tanto Python/Flask quanto Node.js/Express, mas as regras podem ser aplicadas a outros frameworks semelhantes.

---

### Desafios Encontrados

O principal desafio foi equilibrar generalização e precisão.

Regras muito genéricas podem gerar falsos positivos, enquanto regras muito específicas limitam a reutilização da skill.

Outro desafio foi evitar over-engineering. As primeiras versões tendiam a introduzir camadas extras, como Services obrigatórios. Após revisar os requisitos do desafio, a arquitetura alvo foi simplificada para MVC, mantendo a camada de Services como opcional.

Também foi necessário garantir que a refatoração preservasse o comportamento original da aplicação. Para isso, a skill realiza um inventário de endpoints antes das alterações e utiliza essas informações durante a validação final.

## Resultados

### Resumo dos Relatórios de Auditoria

| Projeto | Stack | CRITICAL | HIGH | MEDIUM | LOW | Total | Resolvidos | Status |
|---------|-------|:--------:|:----:|:------:|:---:|:-----:|:----------:|:------:|
| code-smells-project | Python/Flask | 5 | 5 | 4 | 3 | **17** | 17 (100%) | ✅ PASS |
| ecommerce-api-legacy | Node.js/Express | 3 | 5 | 5 | 2 | **15** | 11 (73%) | ✅ PASS |
| task-manager-api | Python/Flask | 2 | 5 | 5 | 3 | **15** | 13 (87%) | ✅ PASS |

Findings não resolvidos são os que estão **fora do escopo MVC** — autenticação real (JWT), logging estruturado (winston/pino) e validação de cartão via gateway externo. Todos os contratos de API foram preservados.

---

### Comparação Antes/Depois

#### Projeto 1 — code-smells-project (Python/Flask E-commerce)

**Antes** — `PARTIAL_MVC`: 4 arquivos (~490 LOC), SQL embutido nas funções, sem separação real de camadas

```
code-smells-project/
├── app.py           (registro de rotas via add_url_rule)
├── controllers.py   (lógica de negócio + SQL + print())
├── models.py        (SQL + regras de desconto + N+1 queries)
└── database.py
```

**Depois** — `MVC` completo: config/, models/, services/, controllers/, routes/ com Flask Blueprints

```
code-smells-project/
├── app.py
├── config/
│   ├── settings.py     (SECRET_KEY, DEBUG, DATABASE_PATH via os.environ)
│   └── database.py     (singleton de conexão SQLite)
├── models/
│   ├── product.py      (queries parametrizadas — sem SQL Injection)
│   ├── user.py         (campo senha excluído por padrão)
│   ├── order.py        (JOIN único — elimina N+1)
│   └── health.py
├── services/
│   ├── product_service.py
│   ├── user_service.py
│   ├── auth_service.py
│   ├── order_service.py    (transação explícita com rollback)
│   └── report_service.py   (constantes LIMIAR_* nomeadas)
├── controllers/
│   ├── product_controller.py
│   ├── user_controller.py
│   ├── auth_controller.py
│   ├── order_controller.py
│   └── system_controller.py
└── routes/
    ├── product_routes.py
    ├── user_routes.py
    ├── order_routes.py
    ├── auth_routes.py
    └── system_routes.py
```

---

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express LMS)

**Antes** — `MONOLITHIC`: 3 arquivos (~182 LOC), AppManager concentrava DB + rotas + lógica

```
ecommerce-api-legacy/src/
├── app.js          (apenas require + listen)
├── AppManager.js   (God Class: initDb + setupRoutes + lógica de checkout + relatório)
└── utils.js        (credenciais hardcoded + globalCache sem TTL)
```

**Depois** — `MVC` completo: src/ reorganizado em 6 camadas

```
ecommerce-api-legacy/src/
├── app.js
├── config/
│   └── database.js     (Promise wrappers para sqlite3 + initDb() assíncrono)
├── models/
│   ├── user.model.js
│   ├── course.model.js
│   ├── enrollment.model.js
│   ├── payment.model.js
│   └── auditLog.model.js
├── services/
│   ├── checkout.service.js   (transação atômica com async/await)
│   ├── financial.service.js  (JOIN único — elimina N+1)
│   └── user.service.js       (cascade delete em transação)
├── controllers/
│   ├── checkout.controller.js
│   ├── financial.controller.js
│   └── user.controller.js
├── routes/
│   ├── checkout.routes.js
│   ├── financial.routes.js
│   └── user.routes.js
└── utils/
    └── crypto.js       (bcrypt substituindo badCrypto())
```

---

#### Projeto 3 — task-manager-api (Python/Flask Task Manager)

**Antes** — `PARTIAL_MVC`: models/, services/ e utils/ existiam, mas routes/ concentrava toda a lógica (~736 LOC) e não havia config/ nem controllers/

```
task-manager-api/
├── app.py
├── database.py
├── models/   (user.py, task.py, category.py)
├── routes/   ← 736 LOC com lógica de negócio embutida, MD5, credenciais hardcoded
├── services/ (existia mas incompleto)
└── utils/    (helpers com código morto não utilizado)
```

**Depois** — `MVC` completo: config/ e controllers/ adicionados; routes/ reduzidas de **736 → 35 LOC**

```
task-manager-api/
├── app.py              (34 LOC — apenas init + blueprints)
├── database.py
├── config/
│   └── settings.py     (os.environ — sem hardcoded)
├── models/
│   ├── user.py         (werkzeug.security — sem MD5)
│   ├── task.py
│   └── category.py
├── controllers/
│   ├── user_controller.py    (70 LOC)
│   ├── task_controller.py    (61 LOC)
│   └── report_controller.py  (54 LOC)
├── routes/
│   ├── user_routes.py        (12 LOC)
│   ├── task_routes.py        (12 LOC)
│   └── report_routes.py      (11 LOC)   ← total: 35 LOC
├── services/
│   ├── user_service.py       (joinedload, validações centralizadas)
│   ├── task_service.py       (is_overdue() único, N+1 eliminado)
│   ├── report_service.py
│   └── notification_service.py
└── utils/
    └── helpers.py      (44 LOC — dead code removido)
```

---

### Checklists de Validação

#### Projeto 1 — code-smells-project (Python/Flask)

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [x] Linguagem detectada corretamente       → Python 3.x
- [x] Framework detectado corretamente       → Flask 3.1.1
- [x] Domínio da aplicação descrito          → E-COMMERCE (produtos, pedidos, usuários)
- [x] Número de arquivos analisados          → 4 arquivos (~490 LOC)

### Fase 2 — Auditoria
- [x] Relatório segue o template definido
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados     → 17 findings (5 CRITICAL)
- [x] Detecção de APIs deprecated            → N/A (nenhuma deprecated detectada)
- [x] Skill pausou e pediu confirmação antes da Fase 3

### Fase 3 — Refatoração
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para config/settings.py
- [x] Models criados (product, user, order, health)
- [x] Routes separadas com Flask Blueprints por domínio
- [x] Controllers concentram orquestração HTTP
- [x] Error handling centralizado com try/except + rollback
- [x] Entry point claro (app.py — apenas init + blueprints)
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem corretamente (21/21 verificações)
```

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [x] Linguagem detectada corretamente       → JavaScript (Node.js)
- [x] Framework detectado corretamente       → Express.js 4.18.2
- [x] Domínio da aplicação descrito          → LMS/E-commerce (checkout de cursos)
- [x] Número de arquivos analisados          → 3 arquivos (~182 LOC)

### Fase 2 — Auditoria
- [x] Relatório segue o template definido
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados     → 15 findings (3 CRITICAL)
- [x] Detecção de APIs deprecated            → ✅ sqlite3 callback API detectada
- [x] Skill pausou e pediu confirmação antes da Fase 3

### Fase 3 — Refatoração
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para config/database.js + .env
- [x] Models criados (user, course, enrollment, payment, auditLog)
- [x] Routes separadas por domínio (checkout, financial, user)
- [x] Controllers concentram orquestração HTTP
- [x] Error handling centralizado com try/catch + status codes semânticos
- [x] Entry point claro (src/app.js)
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem corretamente (3/3 endpoints preservados)
```

#### Projeto 3 — task-manager-api (Python/Flask)

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [x] Linguagem detectada corretamente       → Python 3
- [x] Framework detectado corretamente       → Flask 3.0.0
- [x] Domínio da aplicação descrito          → TASK MANAGEMENT (tasks, users, categories)
- [x] Número de arquivos analisados          → 10 arquivos Python (~1.059 LOC)

### Fase 2 — Auditoria
- [x] Relatório segue o template definido
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados     → 15 findings (2 CRITICAL)
- [x] Detecção de APIs deprecated            → ✅ SQLAlchemy 2.0 + Python 3.12
- [x] Skill pausou e pediu confirmação antes da Fase 3

### Fase 3 — Refatoração
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para config/settings.py
- [x] Models mantidos e melhorados (werkzeug.security, sem MD5)
- [x] Routes reduzidas para registro declarativo (35 LOC total)
- [x] Controllers criados (user, task, report)
- [x] Error handling centralizado nos services com rollback
- [x] Entry point claro (app.py — 34 LOC)
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem corretamente (22/22 endpoints)
```

---

### Aplicações Rodando Após Refatoração

#### Projeto 1 — code-smells-project

```
$ python -c "from app import app; print('Boot OK')"
Boot OK

$ flask run
 * Running on http://127.0.0.1:5000

GET /health
→ 200 {"counts": {"pedidos": 1, "produtos": 10, "usuarios": 4},
        "database": "connected", "status": "ok", "versao": "1.0.0"}

GET /
→ 200 {"endpoints": {"health": "/health", "login": "/login",
        "pedidos": "/pedidos", "produtos": "/produtos",
        "relatorios": "/relatorios/vendas", "usuarios": "/usuarios"},
        "mensagem": "Bem-vindo à API da Loja", "versao": "1.0.0"}

GET /produtos
→ 200 [lista com 10 produtos — sem SQL Injection, sem campo senha exposto]

GET /usuarios
→ 200 [lista com 4 usuários — campo senha ausente da resposta]
```

#### Projeto 2 — ecommerce-api-legacy

```
$ node src/app.js
Frankenstein LMS rodando na porta 3000...

GET /api/admin/financial-report
→ 200 [{"course":"Clean Architecture","revenue":997,
         "students":[{"student":"Leonan","paid":997}]},
        {"course":"Docker","revenue":0,"students":[]}]

POST /api/checkout (cartão válido — número começa com 4)
→ 200 {"msg":"Sucesso","enrollment_id":2}

POST /api/checkout (cartão inválido — número começa com 5)
→ 400 "Pagamento recusado"

DELETE /api/users/1
→ 200 "Usuário deletado com sucesso."

GET /api/admin/financial-report (após delete — cascade validado)
→ 200 [{"course":"Clean Architecture","revenue":997,...}]
```

#### Projeto 3 — task-manager-api

```
$ python seed.py
Seed concluído com sucesso!
  3 usuários
  4 categorias
  10 tasks

$ python app.py
 * Running on http://0.0.0.0:5000

GET /health
→ 200 {"status": "ok", "timestamp": "2026-06-20 22:20:35.452530"}

GET /
→ 200 {"message": "Task Manager API", "version": "1.0"}

GET /tasks
→ 200 [10 tasks com campos user_name e category_name via joinedload — sem N+1 queries]

GET /users
→ 200 [3 usuários — campo password AUSENTE na resposta]

GET /tasks/stats
→ 200 {"cancelled": 1, "completion_rate": 10.0, "done": 1,
        "in_progress": 2, "overdue": 2, "pending": 6, "total": 10}

GET /categories
→ 200 [4 categorias com task_count]

GET /tasks/search?status=pending
→ 200 [6 tasks com status pending]

GET /reports/summary
→ 200 {"overview": {"total_tasks": 10, ...}, "tasks_by_status": {...},
        "tasks_by_priority": {...}, "user_productivity": [...]}

POST /login  {"email": "joao@email.com", "password": "1234"}
→ 200 {"message": "Login realizado com sucesso",
        "user": {"name": "João Silva", "role": "admin"},
        "token": "fake-jwt-token-1"}

POST /login  {"email": "joao@email.com", "password": "errada"}
→ 401 {"error": "Credenciais inválidas"}

GET /tasks/9999
→ 404 {"error": "Task não encontrada"}
```

---

### Observações sobre a Skill em Stacks Diferentes

**Detecção de stack funcionou nos 3 projetos sem ajuste manual.** A heurística baseada em extensões de arquivo + presença de `package.json` (Node.js) vs `requirements.txt` (Python) foi suficiente para discriminar corretamente.

**Estratégia de migração variou por projeto:**

| Projeto | Arquitetura inicial | Estratégia adotada |
|---------|---------------------|--------------------|
| code-smells-project | PARTIAL_MVC (4 arquivos) | Reescrita por camada com SQL parametrizado |
| ecommerce-api-legacy | MONOLITHIC (God Class) | Full Rewrite — AppManager dissolvido em 6 camadas |
| task-manager-api | PARTIAL_MVC (organização parcial) | Incremental — código movido, não reescrito |

**Ponto mais sensível: projetos com organização parcial (Projeto 3).** A skill detectou corretamente que modelos e serviços já existiam e adotou estratégia incremental — adicionando `config/` e `controllers/`, e emagrecendo `routes/` — em vez de reescrever o que já estava correto. Isso exigiu que os arquivos de referência distinguissem explicitamente entre "Full Rewrite" e "Incremental".

**Detecção de APIs deprecated variou por stack:**
- Python (Projeto 1): nenhuma deprecated detectada (Flask 3.1.1 + sqlite3 puros)
- Node.js (Projeto 2): sqlite3 callback API detectada e encapsulada em Promise wrappers
- Python (Projeto 3): SQLAlchemy 2.0 (`Model.query.get` → `db.session.get`) + Python 3.12 (`datetime.utcnow`)

**O ponto de confirmação da Fase 2 foi o mais importante.** Em todos os 3 projetos, o relatório de auditoria foi apresentado antes de qualquer modificação, permitindo revisar os findings e decidir sobre os que estavam fora do escopo MVC (autenticação, gateway de pagamento, logging estruturado).

## Como Executar

### Projeto 1

```
cd code-smells-project
claude "/refactor-arch"
```

### Projeto 2

```
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

### Projeto 3
```
cd ../task-manager-api
claude "/refactor-arch"
```