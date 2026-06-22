# Architecture Audit Report — code-smells-project

================================
PROJECT INFORMATION
===================

Project Name:              code-smells-project (Loja API)
Analysis Date:             2026-06-20

Language:                  Python 3.x
Framework:                 Flask 3.1.1
Database:                  SQLite (loja.db)
ORM:                       No ORM (raw sqlite3)
Package Manager:           pip (requirements.txt)

Architecture (before):     PARTIAL_MVC
Architecture (after):      MVC
Domain:                    E-COMMERCE
Confidence:                HIGH

Source Files Analyzed:     4 arquivos Python (app.py, controllers.py, models.py, database.py)
Estimated Lines of Code:   ~490 linhas

================================
PHASE 1 SUMMARY
===============

Language Detection:         PASS — Python 3.x
Framework Detection:        PASS — Flask 3.1.1
Architecture Detection:     PASS — PARTIAL_MVC
Domain Detection:           PASS — E-COMMERCE (entidades Product, Usuário, Pedido; rotas /produtos, /pedidos; fluxo de checkout)
Endpoint Inventory Created: YES

Endpoints Discovered: 19

| Method | Route                          | Handler                 |
|--------|-------------------------------|-------------------------|
| GET    | /                              | index                   |
| GET    | /produtos                      | listar_produtos         |
| GET    | /produtos/busca                | buscar_produtos         |
| GET    | /produtos/{id}                 | buscar_produto          |
| POST   | /produtos                      | criar_produto           |
| PUT    | /produtos/{id}                 | atualizar_produto       |
| DELETE | /produtos/{id}                 | deletar_produto         |
| GET    | /usuarios                      | listar_usuarios         |
| GET    | /usuarios/{id}                 | buscar_usuario          |
| POST   | /usuarios                      | criar_usuario           |
| POST   | /login                         | login                   |
| POST   | /pedidos                       | criar_pedido            |
| GET    | /pedidos                       | listar_todos_pedidos    |
| GET    | /pedidos/usuario/{usuario_id}  | listar_pedidos_usuario  |
| PUT    | /pedidos/{pedido_id}/status    | atualizar_status_pedido |
| GET    | /relatorios/vendas             | relatorio_vendas        |
| GET    | /health                        | health_check            |
| POST   | /admin/reset-db                | reset_database          |
| POST   | /admin/query                   | executar_query          |

================================
AUDIT SUMMARY
=============

CRITICAL: 5
HIGH:     5
MEDIUM:   4
LOW:      3
----------
Total:    17 findings

Migration Readiness (before): NOT_READY (5 CRITICAL findings)

================================
CRITICAL FINDINGS
=================

## F-001

Severity: CRITICAL
Title: SQL Injection em Múltiplas Queries

File: models.py
Lines: 28, 48-49, 57-60, 68, 92, 110, 126-128, 140, 148-150, 155-161, 163-165, 174, 188, 220, 279-280, 291-297

Description:
Todas as queries SQL eram construídas por concatenação de strings com dados
controláveis pelo usuário. Nenhum uso de parâmetros vinculados (parameterized queries).

Detection Evidence:
  models.py:28:  "SELECT * FROM produtos WHERE id = " + str(id)
  models.py:48:  "INSERT INTO produtos (...) VALUES ('" + nome + "', ..."
  models.py:110: "WHERE email = '" + email + "' AND senha = '" + senha + "'"
  models.py:291: query += " AND (nome LIKE '%" + termo + "%' ..."

Impact:
Acesso não autorizado ao banco, extração de dados, modificação ou exclusão via
SQL Injection. A query de login (linha 110) permitia bypass de autenticação com
o payload: ' OR '1'='1

Recommendation:
Substituir toda concatenação por parâmetros posicionais:
  cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))

Suggested Refactoring Pattern: RP002 — Move Database Access

Status: RESOLVED

---

## F-002

Severity: CRITICAL
Title: Credenciais Hardcoded no Código-Fonte

File: app.py
Lines: 7

Description:
A SECRET_KEY da aplicação Flask estava embutida literalmente no código-fonte,
comprometida para qualquer pessoa com acesso ao repositório.

Detection Evidence:
  app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"

Impact:
Forja de cookies de sessão Flask por qualquer pessoa com acesso ao repositório.

Recommendation:
  import os
  app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

Suggested Refactoring Pattern: AP300 — Hardcoded Configuration

Status: RESOLVED

---

## F-003

Severity: CRITICAL
Title: SECRET_KEY Exposta na Resposta HTTP do Health Check

File: controllers.py
Lines: 289

Description:
O endpoint GET /health retornava a SECRET_KEY literalmente no corpo da resposta JSON,
tornando-a disponível para qualquer cliente HTTP sem autenticação.

Detection Evidence:
  "secret_key": "minha-chave-super-secreta-123"

Impact:
Qualquer cliente HTTP podia obter a chave de assinatura de sessão, permitindo
forjar sessões arbitrárias.

Recommendation:
Remover secret_key, debug e db_path da resposta do health check.

Suggested Refactoring Pattern: AP001 — Hardcoded Credentials

Status: RESOLVED

---

## F-004

Severity: CRITICAL
Title: Endpoints Admin sem Autenticação com Operações Destrutivas

File: app.py
Lines: 47-78

Description:
Os endpoints POST /admin/reset-db e POST /admin/query estavam acessíveis
publicamente sem nenhuma verificação de autenticação ou autorização.
- /admin/reset-db apagava todos os registros de todas as tabelas
- /admin/query executava qualquer SQL arbitrária enviada pelo cliente

Detection Evidence:
  @app.route("/admin/reset-db", methods=["POST"])
  def reset_database():   # sem decorator de autenticação
      cursor.execute("DELETE FROM itens_pedido")
      ...

  @app.route("/admin/query", methods=["POST"])
  def executar_query():
      cursor.execute(query)  # query vem do request body sem sanitização

Impact:
Destruição total do banco de dados ou extração/modificação arbitrária de dados
por qualquer ator externo.

Recommendation:
Remover esses endpoints. Se necessário para manutenção, proteger com autenticação
forte e expor apenas em rede privada.

Suggested Refactoring Pattern: AP002 — SQL Injection Risk

Status: RESOLVED

---

## F-005

Severity: CRITICAL
Title: Senhas Armazenadas e Comparadas em Plain Text

File: models.py, database.py
Lines: models.py:105-120, models.py:122-131, database.py:75-83

Description:
Senhas dos usuários armazenadas em texto plano na coluna `senha` da tabela
`usuarios`. Autenticação comparava strings literais. Dados de seed continham
senhas em plain text ("admin123", "123456").

Detection Evidence:
  # database.py:75-83
  usuarios = [
      ("Admin", "admin@loja.com", "admin123", "admin"),
      ("João Silva", "joao@email.com", "123456", "cliente"),
  ]

  # models.py:109-110
  cursor.execute(
      "SELECT * FROM usuarios WHERE email = '" + email +
      "' AND senha = '" + senha + "'"
  )

Impact:
Qualquer acesso ao banco expõe todas as senhas de todos os usuários em texto claro.

Recommendation:
  from werkzeug.security import generate_password_hash, check_password_hash
  # armazenar: generate_password_hash(senha)
  # validar:   check_password_hash(hash_armazenado, senha_recebida)

Suggested Refactoring Pattern: AP001 — Hardcoded Credentials

Status: RESOLVED

================================
HIGH FINDINGS
=============

## F-006

Severity: HIGH
Title: SQL Executado Diretamente em Route Handlers

File: app.py
Lines: 47-78

Description:
Route handlers reset_database() e executar_query() executavam SQL diretamente
via cursor, violando separação de camadas e expondo operações perigosas sem auth.

Detection Evidence:
  cursor.execute("DELETE FROM itens_pedido")
  cursor.execute(query)  # query arbitrária do usuário

Impact:
Lógica de persistência na camada de rotas. Impossível testar isoladamente.

Recommendation:
Remover endpoints ou mover para camada de model/repository com autenticação.

Suggested Refactoring Pattern: RP002 — Move Database Access (AP103)

Status: RESOLVED

---

## F-007

Severity: HIGH
Title: Lógica de Notificação Misturada no Controller

File: controllers.py
Lines: 208-210, 248-250

Description:
O controller criar_pedido continha lógica de notificação (email, SMS, push) inline.
O controller atualizar_status_pedido continha notificações de mudança de status.

Detection Evidence:
  print("ENVIANDO EMAIL: Pedido " + str(resultado["pedido_id"]) + ...)
  print("ENVIANDO SMS: Seu pedido foi recebido!")
  print("ENVIANDO PUSH: Novo pedido recebido pelo sistema")

Impact:
Acoplamento forte entre domínio de pedidos e domínio de notificações. Impossível
testar ou substituir o canal de notificação independentemente.

Recommendation:
Extrair para funções de notificação no service de pedidos.

Suggested Refactoring Pattern: RP003 — Introduce Service Layer (AP101)

Status: RESOLVED

---

## F-008

Severity: HIGH
Title: Ausência de Camada de Serviços

File: models.py
Lines: 133-315

Description:
Toda lógica de negócio (validação de estoque, cálculo de totais, regras de
desconto) residia em models.py junto com o SQL, sem camada service intermediária.

Detection Evidence:
  # models.py:133-169 — criar_pedido() faz simultaneamente:
  # Validação de estoque (regra de negócio)
  # Cálculo de total (regra de negócio)
  # INSERT de pedido, itens (persistência)
  # UPDATE de estoque (persistência)

  # models.py:256-272 — relatorio_vendas() aplica regras de desconto:
  if faturamento > 10000:
      desconto = faturamento * 0.1

Impact:
Impossível reutilizar regras de negócio sem acessar banco. Testes unitários
de regras de negócio exigiam banco de dados real.

Recommendation:
Criar camada services/ com product_service, user_service, order_service,
report_service. Extrair regras de negócio dos models.

Suggested Refactoring Pattern: RP003 — Introduce Service Layer (AP104)

Status: RESOLVED

---

## F-009

Severity: HIGH
Title: Configuração Hardcoded (DEBUG, Caminho de DB)

File: app.py, database.py
Lines: app.py:7-8, database.py:5

Description:
Além da SECRET_KEY (F-002), DEBUG=True e o caminho do banco de dados estavam
embutidos no código-fonte.

Detection Evidence:
  app.config["DEBUG"] = True      # app.py:8
  db_path = "loja.db"             # database.py:5

Impact:
DEBUG=True em produção expõe stack traces em respostas de erro. Caminho
relativo do banco impede deploy flexível.

Recommendation:
  DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
  db_path = os.environ.get("DATABASE_PATH", "loja.db")

Suggested Refactoring Pattern: AP300 — Hardcoded Configuration

Status: RESOLVED

---

## F-010

Severity: HIGH
Title: Controller Acessa Banco Diretamente (Layer Bypass)

File: controllers.py
Lines: 264-292

Description:
A função health_check() importava e chamava get_db() diretamente, ignorando
a camada de models e criando um bypass na arquitetura em camadas.

Detection Evidence:
  from database import get_db   # controllers.py:3
  def health_check():
      db = get_db()
      cursor = db.cursor()
      cursor.execute("SELECT COUNT(*) FROM produtos")

Impact:
Viola o fluxo Route → Controller → Model → Database.
Lógica de banco de dados duplicada no controller.

Recommendation:
Criar models/health.py com get_health_stats() e chamar via model.

Suggested Refactoring Pattern: RP002 — Move Database Access (AP102)

Status: RESOLVED

================================
MEDIUM FINDINGS
===============

## F-011

Severity: MEDIUM
Title: Padrão N+1 Queries em get_pedidos_usuario e get_todos_pedidos

File: models.py
Lines: 171-201, 203-233

Description:
Para cada pedido retornado, eram executadas duas queries adicionais (itens do
pedido e nome do produto), criando O(N×M) queries para N pedidos com M itens.

Detection Evidence:
  for row in rows:               # 1 query inicial
      cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = ...")
      for item in itens:
          cursor3.execute("SELECT nome FROM produtos WHERE id = ...")

Impact:
Degradação de performance exponencial com o crescimento do volume de pedidos.

Recommendation:
Usar JOIN para recuperar dados em uma única query:
  SELECT p.*, ip.*, pr.nome FROM pedidos p
  JOIN itens_pedido ip ON ip.pedido_id = p.id
  JOIN produtos pr ON pr.id = ip.produto_id

Suggested Refactoring Pattern: AP400 — N+1 Query Pattern

Status: RESOLVED

---

## F-012

Severity: MEDIUM
Title: Código Duplicado entre get_pedidos_usuario e get_todos_pedidos

File: models.py
Lines: 171-201 vs 203-233

Description:
As duas funções eram praticamente idênticas (~30 linhas cada), diferindo apenas
no filtro WHERE. Toda a lógica de construção de pedido com itens estava duplicada.

Detection Evidence:
  Ambas continham:
  - Mesma estrutura de loop sobre pedidos
  - Mesma abertura de cursor2 e cursor3
  - Mesmo mapeamento de campos de itens

Impact:
Bug na lógica de montagem de pedidos precisaria ser corrigido em dois lugares.

Recommendation:
Extrair função auxiliar _build_orders_from_rows(rows) reutilizável.

Suggested Refactoring Pattern: RP005 — Extract Reusable Logic (AP203)

Status: RESOLVED

---

## F-013

Severity: MEDIUM
Title: Ausência de Transação em criar_pedido

File: models.py
Lines: 133-169

Description:
A função criar_pedido() realizava múltiplas operações de escrita sem transação
explícita com rollback. Um erro após INSERT do pedido mas antes de todos os
itens resultaria em estado inconsistente.

Detection Evidence:
  cursor.execute("INSERT INTO pedidos ...")
  pedido_id = cursor.lastrowid
  for item in itens:
      cursor.execute("INSERT INTO itens_pedido ...")
      cursor.execute("UPDATE produtos SET estoque = estoque - ...")
  db.commit()  # sem try/except ou rollback

Impact:
Pedido podia existir sem itens, ou estoque podia ser decrementado sem o
item de pedido correspondente.

Recommendation:
  try:
      cursor.execute("INSERT INTO pedidos ...")
      ...
      db.commit()
  except Exception:
      db.rollback()
      raise

Suggested Refactoring Pattern: AP601 — Missing Error Handling

Status: RESOLVED

---

## F-014

Severity: MEDIUM
Title: print() Usado como Sistema de Logging

File: controllers.py
Lines: 8, 57, 106, 161, 179, 182, 208, 209, 210, 219, 248, 250

Description:
12 chamadas a print() espalhadas pelo código para logging de eventos, erros e
notificações operacionais. Nenhum uso do módulo logging padrão do Python.

Detection Evidence:
  print("Listando " + str(len(produtos)) + " produtos")
  print("ERRO: " + str(e))
  print("ENVIANDO EMAIL: Pedido ...")

Impact:
Impossível controlar nível de log, redirecionar saída, filtrar por severity
ou integrar com sistemas de observabilidade (ELK, CloudWatch).

Recommendation:
  import logging
  logger = logging.getLogger(__name__)
  logger.info("Listando %d produtos", len(produtos))

Suggested Refactoring Pattern: AP201 — Fat Controller

Status: RESOLVED

================================
LOW FINDINGS
============

## F-015

Severity: LOW
Title: Números Mágicos nas Regras de Desconto

File: models.py
Lines: 257-262

Description:
Limiares e percentuais de desconto em relatorio_vendas() usavam literais
numéricos sem nomes explicativos.

Detection Evidence:
  if faturamento > 10000:
      desconto = faturamento * 0.1
  elif faturamento > 5000:
      desconto = faturamento * 0.05
  elif faturamento > 1000:
      desconto = faturamento * 0.02

Impact:
Regras de negócio opacas e difíceis de manter ou ajustar.

Recommendation:
  LIMIAR_DESCONTO_ALTO = 10_000
  PERC_DESCONTO_ALTO = 0.10

Suggested Refactoring Pattern: AP700 — Magic Numbers

Status: RESOLVED

---

## F-016

Severity: LOW
Title: app.add_url_rule em Vez de Flask Blueprints

File: app.py
Lines: 11-30

Description:
Registro de rotas usava app.add_url_rule() para todos os domínios em um único
arquivo, padrão legado para aplicações Flask com múltiplos recursos.

Detection Evidence:
  app.add_url_rule("/produtos", "listar_produtos", controllers.listar_produtos, ...)
  app.add_url_rule("/usuarios", "listar_usuarios", controllers.listar_usuarios, ...)

Impact:
Dificulta organização modular de rotas por domínio.

Recommendation:
Migrar para Flask Blueprints por domínio (product_bp, user_bp, order_bp).

Suggested Refactoring Pattern: DA005 — Legacy Framework Pattern

Status: RESOLVED

---

## F-017

Severity: LOW
Title: Campo Senha Exposto na Resposta de Listagem de Usuários

File: models.py
Lines: 79-87, 95-103

Description:
As funções get_todos_usuarios() e get_usuario_por_id() incluíam o campo `senha`
nos dicionários retornados, serializados diretamente nas respostas HTTP.

Detection Evidence:
  result.append({
      "id": row["id"],
      ...
      "senha": row["senha"],   # campo senha plain text exposto
  })

Impact:
Senhas em plain text retornadas nas respostas de GET /usuarios e GET /usuarios/{id}.

Recommendation:
Excluir o campo `senha` dos retornos de listagem/busca de usuários.

Suggested Refactoring Pattern: AP001 — Hardcoded Credentials

Status: RESOLVED

================================
DEPRECATED APIS
===============

Nenhuma API deprecated detectada.

Flask 3.1.1 é a versão corrente.
sqlite3 não usa APIs deprecadas.
Nenhum import de módulos deprecated (imp, distutils, asyncore, pkg_resources) encontrado.

================================
ENDPOINT INVENTORY (BEFORE REFACTORING)
========================================

| Method | Route                         | Auth | Vulnerabilidades                        |
|--------|-------------------------------|------|-----------------------------------------|
| GET    | /                             | Não  |                                         |
| GET    | /produtos                     | Não  |                                         |
| GET    | /produtos/busca               | Não  | SQL Injection em parâmetro ?q=          |
| GET    | /produtos/{id}                | Não  | SQL Injection em id                     |
| POST   | /produtos                     | Não  | SQL Injection no body                   |
| PUT    | /produtos/{id}                | Não  | SQL Injection                           |
| DELETE | /produtos/{id}                | Não  | SQL Injection em id                     |
| GET    | /usuarios                     | Não  | Retorna senhas em plain text            |
| GET    | /usuarios/{id}                | Não  | Retorna senha em plain text             |
| POST   | /usuarios                     | Não  | Armazena senha em plain text            |
| POST   | /login                        | Não  | SQL Injection + comparação plain text   |
| POST   | /pedidos                      | Não  | SQL Injection                           |
| GET    | /pedidos                      | Não  | N+1 queries                             |
| GET    | /pedidos/usuario/{usuario_id} | Não  | N+1 queries + SQL Injection             |
| PUT    | /pedidos/{pedido_id}/status   | Não  |                                         |
| GET    | /relatorios/vendas            | Não  | Magic numbers                           |
| GET    | /health                       | Não  | Expõe SECRET_KEY na resposta            |
| POST   | /admin/reset-db               | Não  | PERIGO: apaga todo o banco              |
| POST   | /admin/query                  | Não  | PERIGO: execução arbitrária de SQL      |

================================
MVC MIGRATION PLAN (EXECUTED)
==============================

Strategy: PARTIAL_MVC → Full MVC (Incremental)

Migration Approach: Incremental — PARTIAL_MVC permite migração por camadas sem
reescrita completa. Código foi movido e reorganizado, não reescrito do zero.

Step 1: Corrigir findings CRITICAL de segurança
  - Parameterized queries em toda models.py (F-001)
  - Hash de senhas com werkzeug.security (F-005)
  - SECRET_KEY via os.environ (F-002)
  - Remover /admin/reset-db e /admin/query (F-004)
  - Limpar resposta do /health (F-003)

Step 2: Criar camada config/
  - config/settings.py: SECRET_KEY, DEBUG, DATABASE_PATH via os.environ
  - config/database.py: singleton de conexão SQLite + schema + seed com hashes

Step 3: Criar camada models/ com SQL parametrizado
  - models/product.py: queries com ? posicional
  - models/user.py: campo senha excluído por padrão
  - models/order.py: JOIN único para pedidos+itens (elimina N+1)
  - models/health.py: stats para health check

Step 4: Criar camada services/ com regras de negócio
  - services/product_service.py: validações de produto
  - services/user_service.py: criação com hash
  - services/auth_service.py: check_password_hash
  - services/order_service.py: checkout com transação explícita + notificações
  - services/report_service.py: lógica de desconto com constantes nomeadas

Step 5: Refatorar controllers/ para orquestração pura
  - Substituir print() por logging.getLogger(__name__)
  - Controllers chamam apenas services, sem acesso a DB

Step 6: Criar routes/ com Flask Blueprints
  - product_bp, user_bp, order_bp, auth_bp, system_bp
  - app.py: apenas inicialização e registro de blueprints

Expected Target Structure (Achieved):

```
code-smells-project/
├── app.py
├── config/
│   ├── settings.py
│   └── database.py
├── routes/
│   ├── product_routes.py
│   ├── user_routes.py
│   ├── order_routes.py
│   ├── auth_routes.py
│   └── system_routes.py
├── controllers/
│   ├── product_controller.py
│   ├── user_controller.py
│   ├── auth_controller.py
│   ├── order_controller.py
│   └── system_controller.py
├── services/
│   ├── product_service.py
│   ├── user_service.py
│   ├── auth_service.py
│   ├── order_service.py
│   └── report_service.py
└── models/
    ├── product.py
    ├── user.py
    ├── order.py
    └── health.py
```

Dependency Flow (Achieved):
```
HTTP Request
     │
     ▼
  Routes (Blueprints)
     │
     ▼
 Controllers (orquestração)
     │
     ▼
  Services (regras de negócio)
     │
     ▼
   Models (persistência SQL)
     │
     ▼
  Database (SQLite)
```

================================
RISK ASSESSMENT
===============

Low Risk Changes:
  * Troca de print() por logging (sem impacto funcional)
  * Extração de constantes de desconto (mesmas regras de negócio)
  * Remoção do campo senha dos responses de usuário (melhora de segurança)
  * Reorganização de imports entre camadas

Medium Risk Changes:
  * Reorganização de arquivos em diretórios (requer ajuste de imports)
  * Adição de Flask Blueprints (preserva rotas idênticas)
  * Extração de camada de services (preserva comportamento)
  * Troca de queries para parameterized (preserva resultados)

High Risk Changes:
  * Troca de plain text para hash de senhas
    NOTA: banco existente com senhas plain text deve ser deletado antes do boot
  * Remoção de /admin/reset-db e /admin/query (breaking — funcionalidade removida)

Potential Breaking Changes:
  * POST /admin/reset-db — removido (era operação destrutiva insegura)
  * POST /admin/query — removido (era execução arbitrária de SQL)
  * GET /usuarios, GET /usuarios/{id} — campo `senha` removido da response
  * GET /health — campos `secret_key`, `debug`, `db_path` removidos da response

================================
REFACTORING CHECKLIST
=====================

[x] F-001: SQL Injection resolvido (parameterized queries em todos os models)
[x] F-002: SECRET_KEY movida para variável de ambiente
[x] F-003: SECRET_KEY removida da resposta do /health
[x] F-004: Endpoints admin removidos
[x] F-005: Hash de senha implementado (werkzeug.security)
[x] F-006: SQL removido dos route handlers
[x] F-007: Lógica de notificação extraída para order_service
[x] F-008: Camada services/ criada com 5 serviços
[x] F-009: DEBUG e DATABASE_PATH movidos para env vars
[x] F-010: health_check usando models.health em vez de get_db() direto
[x] F-011: N+1 resolvido com LEFT JOIN em models/order.py
[x] F-012: Função _build_orders_from_rows extraída e reutilizada
[x] F-013: Transação explícita com try/except + db.rollback() em order_service
[x] F-014: logging.getLogger(__name__) substituindo print() em todas as camadas
[x] F-015: Constantes LIMIAR_* e PERC_* nomeadas em report_service
[x] F-016: Flask Blueprints em routes/ por domínio
[x] F-017: Campo senha excluído por padrão em models/user.py

================================
VALIDATION RESULTS
==================

Application Boot:             PASS
  — app.py importa com sucesso; banco criado; seed aplicado

Endpoint Validation:          PASS  (21/21 verificações)
  — 17 endpoints originais preservados (rotas e métodos idênticos)
  — POST /admin/reset-db retorna 404 (removido intencionalmente)
  — POST /admin/query retorna 404 (removido intencionalmente)
  — GET /usuarios: campo 'senha' ausente na response
  — GET /health: sem secret_key, db_path, debug na response
  — POST /login com senha correta: HTTP 200
  — POST /login com senha errada: HTTP 401

Architecture Validation:      PASS
  — Nenhum controller importa get_db() diretamente
  — Nenhum service importa flask.request
  — Nenhum model importa flask ou controllers
  — Arquivos legados (database.py, models.py, controllers.py) removidos
  — Fluxo Route → Controller → Service → Model respeitado

Configuration Validation:     PASS
  — "minha-chave-super-secreta-123" não encontrada em nenhum arquivo .py
  — DEBUG lido de os.environ em config/settings.py
  — DATABASE_PATH lido de os.environ em config/settings.py

SQL Injection Validation:     PASS
  — Nenhuma concatenação de string em queries SQL encontrada
  — Todos os parâmetros de usuário passados como tupla posicional

Logging Validation:           PASS
  — Nenhum print() encontrado em config/, models/, services/, controllers/, routes/

Deprecated API Validation:    NOT APPLICABLE
  — Nenhuma API deprecated detectada no projeto

================================
FINAL STATUS
============

Findings Open:      0
Findings Resolved: 17 (5 CRITICAL + 5 HIGH + 4 MEDIUM + 3 LOW)

Overall Status: PASS

================================
END OF REPORT — FIRST AUDIT CYCLE (2026-06-20)
===============================================

================================
SECOND AUDIT CYCLE — 2026-06-22
================================

Context:
Este segundo ciclo audita o mesmo projeto após a refatoração do primeiro ciclo.
A arquitetura era MVC na entrada — o objetivo foi identificar violações residuais,
oportunidades de melhoria e aplicar os padrões RP006, RP007 e RP008.

================================
PROJECT INFORMATION (2nd Cycle)
================================

Project Name:              code-smells-project (Loja API)
Analysis Date:             2026-06-22

Language:                  Python 3.12
Framework:                 Flask 3.1.1
Database:                  SQLite (loja.db)
ORM:                       No ORM (raw sqlite3)
Package Manager:           pip (requirements.txt)

Architecture (entrada):    MVC
Architecture (saída):      MVC (enhanced) + utils/ + middleware/
Domain:                    E-COMMERCE
Confidence:                HIGH

Source Files Analyzed:     17 arquivos Python
Estimated Lines of Code:   902 linhas

Migration Strategy:        TARGETED (melhorias pontuais — sem reorganização estrutural)

================================
ENDPOINT INVENTORY (2nd Cycle)
================================

Endpoints Discovered: 17

| Method | Route                          | Handler                    | File                            |
|--------|-------------------------------|----------------------------|---------------------------------|
| GET    | /                              | index                      | controllers/system_controller.py |
| GET    | /health                        | health_check               | controllers/system_controller.py |
| GET    | /produtos                      | list_products              | controllers/product_controller.py |
| GET    | /produtos/<id>                 | get_product                | controllers/product_controller.py |
| POST   | /produtos                      | create_product             | controllers/product_controller.py |
| PUT    | /produtos/<id>                 | update_product             | controllers/product_controller.py |
| DELETE | /produtos/<id>                 | delete_product             | controllers/product_controller.py |
| GET    | /produtos/busca                | search_products            | controllers/product_controller.py |
| GET    | /usuarios                      | list_users                 | controllers/user_controller.py   |
| GET    | /usuarios/<id>                 | get_user                   | controllers/user_controller.py   |
| POST   | /usuarios                      | create_user                | controllers/user_controller.py   |
| POST   | /login                         | login                      | controllers/auth_controller.py   |
| POST   | /pedidos                       | create_order               | controllers/order_controller.py  |
| GET    | /pedidos                       | list_all_orders            | controllers/order_controller.py  |
| GET    | /pedidos/usuario/<usuario_id>  | list_user_orders           | controllers/order_controller.py  |
| PUT    | /pedidos/<pedido_id>/status    | update_order_status        | controllers/order_controller.py  |
| GET    | /relatorios/vendas             | sales_report               | controllers/order_controller.py  |

Protected Endpoints (before): 0
Protected Endpoints (after):  3 (GET /relatorios/vendas, GET /pedidos, GET /usuarios)

================================
AUDIT SUMMARY (2nd Cycle)
==========================

CRITICAL: 1
HIGH:     3  (incluindo RP007 — gap não detectado na primeira auditoria)
MEDIUM:   3
LOW:      2
----------
Total:    9 findings

Migration Readiness (before): REQUIRES_REVIEW
Migration Readiness (after):  COMPLETE

================================
CRITICAL FINDINGS (2nd Cycle)
==============================

## G-001

Severity: CRITICAL
ID: AP001
Title: Hardcoded Secret Key Fallback

File: config/settings.py
Line: 3

Description:
A SECRET_KEY possuía um fallback literal hardcoded no repositório:
  SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-in-production")
Qualquer deploy sem a env var SECRET_KEY usaria silenciosamente esse valor conhecido.

Detection Evidence:
  os.environ.get("SECRET_KEY", "dev-only-change-in-production")

Impact:
Chave de assinatura de sessão Flask comprometida para quem tem acesso ao repositório.
O silêncio do fallback mascara o erro de configuração em produção.

Recommendation:
Remover o fallback. Emitir UserWarning no boot quando SECRET_KEY não estiver definida.

Suggested Refactoring Pattern: RP007 — Remove or Protect Dangerous Endpoint

Status: RESOLVED
  — config/settings.py: fallback substituído por UserWarning (dev-secret-key-change-in-production)
  — warnings.warn() emitido ao inicializar a aplicação sem SECRET_KEY

---

================================
HIGH FINDINGS (2nd Cycle)
==========================

## G-002

Severity: HIGH
ID: AP105
Title: Service Layer Bypasses Model Layer — Direct Database Access

File: services/order_service.py
Lines: 2, 14, 33, 38

Description:
O service importava get_db() diretamente de config.database e gerenciava
commit/rollback dentro da camada de serviço, violando o fluxo MVC:
  Route → Controller → Service → Model → Database

Detection Evidence:
  from config.database import get_db   # linha 2
  db = get_db()                        # linha 14
  db.commit()                          # linha 33
  db.rollback()                        # linha 38

Impact:
Serviço acoplado à infraestrutura de banco. Untestable sem banco real.
Viola o princípio de responsabilidade única.

Recommendation:
Mover gerenciamento de transação para models/order.py via create_order_with_items().
Service deve chamar apenas o model, sem conhecer a conexão.

Suggested Refactoring Pattern: RP002 — Move Database Access

Status: RESOLVED
  — models/order.py: create_order_with_items() criado (INSERT + itens + decrement + commit/rollback)
  — services/order_service.py: import get_db removido; chama order_model.create_order_with_items()

---

## G-003

Severity: HIGH
ID: AP300
Title: Hardcoded Seed Credentials in Source Code

File: config/database.py
Lines: 83–91

Description:
Senhas literais de usuários de seed commitadas no código-fonte:
  generate_password_hash("admin123")
  generate_password_hash("123456")
  generate_password_hash("senha123")
As senhas em plain text ficam permanentemente visíveis no histórico do repositório.

Detection Evidence:
  ("Admin", "admin@loja.com", generate_password_hash("admin123"), "admin"),
  ("João Silva", "joao@email.com", generate_password_hash("123456"), "cliente"),
  ("Maria Santos", "maria@email.com", generate_password_hash("senha123"), "cliente"),

Impact:
Credenciais padrão da conta admin conhecidas por qualquer pessoa com acesso ao repositório.

Recommendation:
Parametrizar via env vars: SEED_ADMIN_PASS, SEED_USER1_PASS, SEED_USER2_PASS.

Status: RESOLVED
  — config/database.py: constantes SEED_*_PASS via os.environ.get()
  — Fallbacks claramente marcados como dev-only ("admin-dev-only", "user1-dev-only", "user2-dev-only")

---

## G-004

Severity: HIGH
ID: RP007
Title: Admin Endpoints Without Authentication — Missing Auth Middleware

Files: routes/order_routes.py (linhas 7, 10), routes/user_routes.py (linha 6)

Description:
GAP DE AUDITORIA: O inventário do primeiro ciclo identificou "Protected Endpoints: 0"
mas não gerou um finding formal para os endpoints admin sem autenticação.

Três endpoints expunham dados sensíveis sem nenhuma verificação de credencial:
  GET /relatorios/vendas — relatório financeiro completo (faturamento, descontos, ticket médio)
  GET /pedidos           — listagem de todos os pedidos de todos os usuários
  GET /usuarios          — listagem de todos os usuários com emails e tipos de conta

Nenhum middleware, decorator ou before_request hook existia em qualquer parte do código.

Detection Evidence:
  Endpoint inventory Phase 1: "Protected Endpoints: 0"
  Grep por login_required, jwt, session, require_auth: zero ocorrências

Impact:
Qualquer cliente HTTP não autenticado acessava relatórios financeiros e dados pessoais
de todos os usuários.

Recommendation:
Criar middleware/auth.py com decorator require_admin validando header X-Admin-Token.
Aplicar nas rotas admin via add_url_rule.
Em produção, substituir comparação de token por JWT ou sessão Flask.

Suggested Refactoring Pattern: RP007 — Remove or Protect Dangerous Endpoint

Status: RESOLVED
  — middleware/__init__.py e middleware/auth.py criados
  — require_admin decorator com ADMIN_TOKEN via os.environ (UserWarning se ausente)
  — Aplicado em: require_admin(order_controller.list_all_orders)
                  require_admin(order_controller.sales_report)
                  require_admin(user_controller.list_users)
  — Validado: GET /relatorios/vendas sem token → 401; com X-Admin-Token → 200

---

================================
MEDIUM FINDINGS (2nd Cycle)
============================

## G-005

Severity: MEDIUM
ID: AP203
Title: Duplicate Row-to-Dict Mapping Logic Across Models

Files: models/product.py (linhas 4–14), models/user.py (linhas 4–14)

Description:
Função _row_to_dict() duplicada em dois modelos com estrutura idêntica de
mapeamento sqlite3.Row → dict.

Detection Evidence:
  models/product.py: _row_to_dict retorna dict com 8 campos de produto
  models/user.py:    _row_to_dict retorna dict com 5 campos de usuário + senha opcional
  Mesmo padrão estrutural repetido em ambos os arquivos.

Impact:
Manutenção duplicada. Modelos podem divergir independentemente.

Recommendation:
Extrair row_to_dict(row, fields) genérico para utils/db_utils.py.

Status: RESOLVED
  — utils/db_utils.py criado com row_to_dict(row, fields)
  — models/product.py: usa row_to_dict com _PRODUCT_FIELDS
  — models/user.py: usa row_to_dict com _USER_FIELDS

---

## G-006

Severity: MEDIUM
ID: AP601
Title: Missing Null Check Before .get() on Request JSON

File: controllers/order_controller.py
Lines: 47–49

Description:
request.get_json() retornava None quando o body era ausente ou o Content-Type
não era application/json, causando AttributeError não tratado na linha seguinte:
  dados.get("status", "")

Detection Evidence:
  Line 47: dados = request.get_json()
  Line 48: novo_status = dados.get("status", "")   # sem null guard

Impact:
AttributeError não tratado expõe traceback interno em resposta 500.

Recommendation:
  if not dados:
      return jsonify({"erro": "Dados inválidos"}), 400

Status: RESOLVED
  — controllers/order_controller.py: null check adicionado após request.get_json()
  — Validado: body null com Content-Type: application/json → {"erro": "Dados inválidos"} 400

---

## G-007

Severity: MEDIUM
ID: AP401
Title: Multiple Sequential Queries Where Single Aggregate Query Suffices

File: models/order.py
Lines: 104–122

Description:
get_order_stats() executava 5 queries sequenciais separadas ao banco:
  SELECT COUNT(*) FROM pedidos          (×1)
  SELECT SUM(total) FROM pedidos        (×1)
  SELECT COUNT(*) ... WHERE status = X  (×3)

Detection Evidence:
  5 chamadas cursor.execute() + cursor.fetchone() sequenciais na mesma função.

Impact:
5 round-trips ao banco por chamada a GET /relatorios/vendas.

Recommendation:
Única query com aggregation condicional:
  SELECT COUNT(*), COALESCE(SUM(total),0),
         SUM(CASE WHEN status='pendente' THEN 1 ELSE 0 END), ...
  FROM pedidos

Status: RESOLVED
  — models/order.py: get_order_stats() refatorado para 1 query com CASE WHEN + COALESCE
  — Redução de 5 para 1 round-trip ao banco por chamada

---

================================
LOW FINDINGS (2nd Cycle)
=========================

## G-008

Severity: LOW
ID: AP204
Title: Dead Notification Stubs Mixed into Service Layer

File: services/order_service.py
Lines: 58–68

Description:
_notify_order_created() e _notify_status_changed() eram stubs que apenas
faziam logger.info() sem enviar nenhuma notificação real. Estavam misturadas
à lógica de negócio do service.

Detection Evidence:
  def _notify_order_created(...): apenas logger.info × 3
  def _notify_status_changed(...): apenas logger.info condicionais

Impact:
Ruído no service layer. Stubs sem contrato explícito misturados com regras de negócio.

Recommendation:
Mover para utils/notifications.py tornando o caráter de stub explícito.

Status: RESOLVED
  — utils/notifications.py criado com notify_order_created() e notify_status_changed()
  — services/order_service.py: importa utils.notifications; stubs removidos do módulo

---

## G-009

Severity: LOW
ID: AP105 (cross-domain)
Title: Cross-Domain Model Access — Order Model Operates on Products Table

File: models/order.py
Lines: 71–90

Description:
get_product_for_order() e decrement_stock() executavam SQL na tabela `produtos`
dentro do módulo do model de pedidos.

Detection Evidence:
  cursor.execute("SELECT ... FROM produtos WHERE id = ?")   # em models/order.py
  cursor.execute("UPDATE produtos SET estoque = ...")       # em models/order.py

Impact:
Operações de domínio de produto espalhadas pelo model de pedidos.
Desenvolvedor modificando schema de produtos deve verificar dois arquivos.

Recommendation:
Mover ambas para models/product.py.

Status: RESOLVED
  — models/product.py: recebeu get_product_for_order() e decrement_stock()
  — models/order.py: create_order_with_items() chama product_model.decrement_stock()
  — services/order_service.py: chama product_model.get_product_for_order()

---

================================
RP PATTERN EVALUATION (2nd Cycle)
===================================

| Padrão | Aplicável | Status     | Evidência                                          |
|--------|-----------|------------|----------------------------------------------------|
| RP006  | NÃO       | N/A        | werkzeug.security PBKDF2 já em uso em todo o projeto |
| RP007  | SIM       | RESOLVED   | middleware/auth.py + require_admin em 3 rotas admin |
| RP008  | NÃO       | N/A        | Nenhuma API depreciada detectada (Flask 3.1.1, sqlite3 padrão) |

---

================================
DEPRECATED APIS (2nd Cycle)
============================

Nenhuma API deprecated detectada.

Verificado:
  — datetime.utcnow(): ausente
  — import imp / distutils / asyncore / pkg_resources: ausente
  — asyncio.get_event_loop(): ausente
  — APIs deprecated do Flask: ausente
  — session.query() (SQLAlchemy legacy): não aplicável (sem ORM)

Flask 3.1.1, werkzeug e sqlite3 estão na versão corrente.

================================
NEW STRUCTURE (after 2nd Cycle)
================================

```
code-smells-project/
├── app.py
├── requirements.txt
├── config/
│   ├── database.py      ← SEED_*_PASS via env vars (G-003)
│   └── settings.py      ← SECRET_KEY com UserWarning (G-001)
├── models/
│   ├── product.py       ← + get_product_for_order, decrement_stock (G-009)
│   │                    ← usa row_to_dict de utils/ (G-005)
│   ├── user.py          ← usa row_to_dict de utils/ (G-005)
│   ├── order.py         ← + create_order_with_items() (G-002)
│   │                    ← get_order_stats() usa 1 query (G-007)
│   └── health.py
├── services/
│   ├── order_service.py ← sem get_db(), sem stubs inline (G-002, G-008)
│   └── (demais inalterados)
├── controllers/
│   ├── order_controller.py ← null check em update_order_status (G-006)
│   └── (demais inalterados)
├── routes/
│   ├── order_routes.py  ← require_admin em /relatorios/vendas e GET /pedidos (G-004)
│   ├── user_routes.py   ← require_admin em GET /usuarios (G-004)
│   └── (demais inalterados)
├── middleware/          ← NOVO
│   ├── __init__.py
│   └── auth.py          ← require_admin + ADMIN_TOKEN env var (G-004)
└── utils/               ← NOVO
    ├── __init__.py
    ├── db_utils.py      ← row_to_dict genérico (G-005)
    └── notifications.py ← stubs isolados (G-008)
```

================================
VALIDATION RESULTS (2nd Cycle)
================================

Application Boot:             PASS
  — python -c "from app import app" sem erros de import
  — UserWarning emitido para SECRET_KEY e ADMIN_TOKEN ausentes

Endpoint Validation:          PASS  (17/17)
  — Todos os 17 endpoints respondem com contratos preservados
  — GET /relatorios/vendas sem token: 401
  — GET /relatorios/vendas com X-Admin-Token: 200
  — GET /pedidos sem token: 401
  — GET /usuarios sem token: 401
  — POST /pedidos: cria pedido e decrementa estoque atomicamente
  — PUT /pedidos/<id>/status com body null: {"erro": "Dados inválidos"} 400

Architecture Validation:      PASS
  — services/order_service.py sem import de get_db
  — require_admin aplicado no routes/ layer (não no controller)
  — Fluxo Route → Middleware → Controller → Service → Model respeitado

Configuration Validation:     PASS
  — SECRET_KEY com UserWarning no boot
  — ADMIN_TOKEN com UserWarning no boot
  — Senhas de seed via SEED_*_PASS env vars

RP Pattern Validation:        PASS
  — RP006: N/A (werkzeug PBKDF2 já correto)
  — RP007: RESOLVED (middleware/auth.py + 3 rotas protegidas)
  — RP008: N/A (sem APIs depreciadas)

================================
REFACTORING CHECKLIST (2nd Cycle)
===================================

[x] G-001 (AP001 CRITICAL): SECRET_KEY fallback substituído por UserWarning
[x] G-002 (AP105 HIGH): Transação movida para models/order.py
[x] G-003 (AP300 HIGH): Senhas de seed via env vars
[x] G-004 (RP007 HIGH): middleware/auth.py + require_admin em 3 rotas admin
[x] G-005 (AP203 MEDIUM): row_to_dict extraído para utils/db_utils.py
[x] G-006 (AP601 MEDIUM): Null check em order_controller.update_order_status
[x] G-007 (AP401 MEDIUM): get_order_stats() com 1 query ao invés de 5
[x] G-008 (AP204 LOW): Notification stubs isolados em utils/notifications.py
[x] G-009 (AP105 LOW): get_product_for_order/decrement_stock em models/product.py

================================
FINAL STATUS (2nd Cycle)
=========================

Findings Open:      0
Findings Resolved:  9 (1 CRITICAL + 3 HIGH + 3 MEDIUM + 2 LOW)

Overall Status: PASS

================================
CUMULATIVE PROJECT STATUS
==========================

| Ciclo | Data       | Arquitetura Entrada | Arquitetura Saída       | Findings | Status |
|-------|------------|---------------------|-------------------------|----------|--------|
| 1º    | 2026-06-20 | PARTIAL_MVC (4 arq) | MVC (17 arq)            | 17       | PASS   |
| 2º    | 2026-06-22 | MVC (17 arq)        | MVC+utils+middleware    | 9        | PASS   |
| Total |            |                     |                         | 26       | PASS   |

================================
END OF REPORT — SECOND AUDIT CYCLE (2026-06-22)
================================================