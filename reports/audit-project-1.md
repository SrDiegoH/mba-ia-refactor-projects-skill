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
END OF REPORT
=============
