# Architecture Audit Report — task-manager-api

---

## PROJECT INFORMATION

| Field | Value |
|-------|-------|
| Project Name | task-manager-api |
| Analysis Date | 2026-06-20 |
| Language | Python 3 |
| Framework | Flask 3.0.0 |
| Database | SQLite (tasks.db) |
| ORM | SQLAlchemy (flask-sqlalchemy 3.1.1) |
| Package Manager | pip / requirements.txt |
| Architecture | Partial MVC (models + routes + services + utils, sem controllers) |
| Domain | Gerenciamento de Tarefas (Task Management) |
| Confidence | High |
| Files Analyzed | 10 |
| Estimated LOC | 1.059 |

---

## PHASE 1 SUMMARY

| Check | Status |
|-------|--------|
| Stack Detection | COMPLETE |
| Architecture Detection | COMPLETE — Partial MVC identificado |
| Domain Detection | COMPLETE — Task Management (High confidence) |
| Endpoint Inventory | COMPLETE — 22 endpoints mapeados |

---

## ENDPOINT INVENTORY SUMMARY

| Metric | Count |
|--------|-------|
| Total Endpoints | 22 |
| GET | 11 |
| POST | 4 |
| PUT | 3 |
| PATCH | 0 |
| DELETE | 4 |
| Protected Endpoints | 0 (autenticação não implementada) |
| Public Endpoints | 22 |

### Inventário Completo

| Method | Route | Handler | File |
|--------|-------|---------|------|
| GET | /users | get_users() | routes/user_routes.py |
| GET | /users/\<id\> | get_user() | routes/user_routes.py |
| GET | /users/\<id\>/tasks | get_user_tasks() | routes/user_routes.py |
| POST | /users | create_user() | routes/user_routes.py |
| PUT | /users/\<id\> | update_user() | routes/user_routes.py |
| DELETE | /users/\<id\> | delete_user() | routes/user_routes.py |
| POST | /login | login() | routes/user_routes.py |
| GET | /tasks | get_tasks() | routes/task_routes.py |
| GET | /tasks/\<id\> | get_task() | routes/task_routes.py |
| GET | /tasks/search | search_tasks() | routes/task_routes.py |
| GET | /tasks/stats | task_stats() | routes/task_routes.py |
| POST | /tasks | create_task() | routes/task_routes.py |
| PUT | /tasks/\<id\> | update_task() | routes/task_routes.py |
| DELETE | /tasks/\<id\> | delete_task() | routes/task_routes.py |
| GET | /reports/summary | summary_report() | routes/report_routes.py |
| GET | /reports/user/\<id\> | user_report() | routes/report_routes.py |
| GET | /categories | get_categories() | routes/report_routes.py |
| POST | /categories | create_category() | routes/report_routes.py |
| PUT | /categories/\<id\> | update_category() | routes/report_routes.py |
| DELETE | /categories/\<id\> | delete_category() | routes/report_routes.py |
| GET | /health | health() | app.py |
| GET | / | index() | app.py |

---

## AUDIT SUMMARY

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 5 |
| MEDIUM | 5 |
| LOW | 3 |
| **Total** | **15** |

---

## CRITICAL FINDINGS

---

### C1

```
ID: AP001

Severity: CRITICAL

Title: Hardcoded Credentials

File: services/notification_service.py

Lines: 9-10

Evidence:
  self.email_user = 'taskmanager@gmail.com'
  self.email_password = 'senha123'
  Credenciais SMTP hardcoded diretamente no código-fonte.

Impact:
  Exposição de credenciais no repositório. Qualquer pessoa com
  acesso ao código pode obter as credenciais de email.

Recommendation:
  Mover para variáveis de ambiente:
  MAIL_USER e MAIL_PASSWORD no arquivo .env
  Usar python-dotenv para carregar (já está em requirements.txt).

Status: OPEN
```

---

### C2

```
ID: AP001 (variant)

Severity: CRITICAL

Title: Insecure Password Hashing — MD5

File: models/user.py

Lines: 27-32

Evidence:
  def set_password(self, pwd):
      self.password = hashlib.md5(pwd.encode()).hexdigest()

  def check_password(self, pwd):
      return self.password == hashlib.md5(pwd.encode()).hexdigest()

  MD5 é criptograficamente quebrado desde 2004. Vulnerável a
  ataques de rainbow table e colisão.

Impact:
  Senhas de todos os usuários podem ser quebradas offline em
  segundos com ferramentas como hashcat ou tabelas rainbow.

Recommendation:
  Substituir por werkzeug.security.generate_password_hash()
  e check_password_hash() — já disponível no Flask sem
  dependências adicionais.

Status: OPEN
```

---

## HIGH FINDINGS

---

### H1

```
ID: AP001 (variant)

Severity: HIGH

Title: Fake Authentication Token

File: routes/user_routes.py

Lines: 210

Evidence:
  'token': 'fake-jwt-token-' + str(user.id)
  Token JWT não implementado — retorna string previsível
  baseada no ID do usuário.

Impact:
  Autenticação não existe. Qualquer chamada de API é anônima.
  Endpoints "protegidos" podem ser bypassados trivialmente.

Recommendation:
  Implementar JWT real com PyJWT ou flask-jwt-extended.
  Fora do escopo imediato do refactor MVC, mas deve ser registrado.

Status: OPEN
```

---

### H2

```
ID: AP100

Severity: HIGH

Title: Business Logic In Routes — Users

File: routes/user_routes.py

Lines: 42-212

Evidence:
  212 linhas contendo: validação de email via regex (linha 61, 106),
  validação de senha (64, 115), validação de role (71, 120),
  cálculo de overdue (171-180), queries diretas ao banco (12, 29, 35,
  67, 94, 109, 136, 155, 197), lógica de cascata de delete (140-142).
  Múltiplas responsabilidades na mesma camada.

Impact:
  Violação de SoC (Separation of Concerns). Impossível testar
  lógica de negócio sem inicializar o Flask.

Recommendation:
  Extrair lógica de negócio para UserService.
  Criar UserController para orquestração HTTP.

Status: OPEN
```

---

### H3

```
ID: AP100

Severity: HIGH

Title: Business Logic In Routes — Tasks

File: routes/task_routes.py

Lines: 11-299

Evidence:
  300 linhas (maior arquivo do projeto) contendo:
  - Cálculo de overdue repetido em 3 locais (30-39, 71-80, 282-287)
  - Validação de domínio (título 3-200 chars: 96-100, 167-170)
  - N+1 queries em loop (41-57): User.query.get() e Category.query.get()
    chamados para cada task na listagem
  - Serialização manual de dicts ao invés de usar to_dict()
  - Status validation hardcoded (110, 177)

Impact:
  Fat route com múltiplas responsabilidades. Performance degradada
  pelo N+1 (O(2n) queries para GET /tasks).

Recommendation:
  Extrair para TaskController + TaskService.
  Corrigir N+1 com joinedload().

Status: OPEN
```

---

### H4

```
ID: AP100

Severity: HIGH

Title: Business Logic In Routes — Reports/Categories

File: routes/report_routes.py

Lines: 12-155

Evidence:
  Cálculos de produtividade por usuário (54-68): loop com contagem
  manual de status. Overdue calculation duplicada (33-43, 132-135).
  Task.query.all() chamado redundantemente para calcular overdue
  quando contagens por status já foram feitas com count() separados.

Impact:
  Lógica de relatório acoplada à camada HTTP. Queries ineficientes
  (Task.query.all() carrega todos os objetos para apenas contar).

Recommendation:
  Extrair para ReportService.
  Usar COUNT direto no banco ao invés de carregar objetos.

Status: OPEN
```

---

### H5

```
ID: AP300

Severity: HIGH

Title: Hardcoded Application Configuration

File: app.py

Lines: 11-13

Evidence:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
  app.config['SECRET_KEY'] = 'super-secret-key-123'
  Valores de configuração de ambiente hardcoded no código-fonte.

Impact:
  Impossível deployar em diferentes ambientes (dev/staging/prod)
  sem modificar o código-fonte. SECRET_KEY fraca exposta.

Recommendation:
  Criar config/settings.py com leitura via os.environ.
  Usar python-dotenv para arquivo .env local.

Status: OPEN
```

---

## MEDIUM FINDINGS

---

### M1

```
ID: AP400

Severity: MEDIUM

Title: N+1 Query Problem — GET /tasks

File: routes/task_routes.py

Lines: 41-57

Evidence:
  for t in tasks:  # Task.query.all() retorna N tasks
      if t.user_id:
          user = User.query.get(t.user_id)      # query #1 por task
      if t.category_id:
          cat = Category.query.get(t.category_id)  # query #2 por task
  Total: 1 + 2N queries para N tasks.

Impact:
  Com 100 tasks: 201 queries por request.
  Com 1000 tasks: 2001 queries por request.
  Degradação severa de performance.

Recommendation:
  Usar joinedload:
  Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
  Reduz para 1-3 queries independente do volume.

Status: OPEN
```

---

### M2

```
ID: AP203

Severity: MEDIUM

Title: Duplicate Code — Overdue Calculation (6 cópias)

Files:
  routes/task_routes.py: 30-39, 71-80, 282-287
  routes/user_routes.py: 171-180
  routes/report_routes.py: 33-43, 132-135

Evidence:
  Bloco idêntico repetido 6 vezes:
  if t.due_date:
      if t.due_date < datetime.utcnow():
          if t.status != 'done' and t.status != 'cancelled':
              [overdue = True]
  O modelo Task já possui método is_overdue() que encapsula
  exatamente esta lógica, mas não é usado.

Impact:
  Bug nesta lógica exige 6 correções em 3 arquivos.

Recommendation:
  Usar task.is_overdue() em todos os lugares.

Status: OPEN
```

---

### M3

```
ID: AP203

Severity: MEDIUM

Title: Duplicate Code — Email Validation

Files:
  routes/user_routes.py: 61, 106
  utils/helpers.py: 19-23

Evidence:
  Regex r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$' duplicada inline
  em duas rotas. Função validate_email() existe em helpers.py
  mas nunca é importada nem chamada.

Impact:
  Utilitário ignorado. Mudança na regra de validação exige
  atualização em 3 lugares.

Recommendation:
  Importar e usar validate_email() de utils/helpers.py.

Status: OPEN
```

---

### M4

```
ID: AP203

Severity: MEDIUM

Title: Duplicate Code — Constants Redefinidas

Files:
  utils/helpers.py: 110-116 (definição)
  routes/task_routes.py: 110, 177 (hardcoded)
  routes/user_routes.py: 71, 120 (hardcoded)

Evidence:
  VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']
  VALID_ROLES = ['user', 'admin', 'manager']
  Definidos em helpers.py e ignorados. Valores hardcoded nas rotas.

Impact:
  Adicionar novo status requer atualização em 3 lugares.

Recommendation:
  Importar constantes de utils/helpers.py.

Status: OPEN
```

---

### M5

```
ID: AP601

Severity: MEDIUM

Title: Missing Structured Error Handling

Files:
  routes/task_routes.py: 62, 137, 152, 204, 237
  routes/user_routes.py: 87-90, 130-132, 149-151
  routes/report_routes.py: 182-188, 204-208, 217-222

Evidence:
  Blocos except: sem tipo específico e sem logging estruturado.
  Uso de print() para logging (ex: "ERRO: {str(e)}").
  Alguns except: completamente vazios (user_routes.py:130).

Impact:
  Erros silenciados em produção. Diagnóstico impossível.
  Stack traces perdidos.

Recommendation:
  Usar logging module ao invés de print().
  Capturar Exception as e explicitamente.
  Considerar handler global de erros no Flask.

Status: OPEN
```

---

## LOW FINDINGS

---

### L1

```
ID: AP204

Severity: LOW

Title: Dead Code — process_task_data() e generate_id()

File: utils/helpers.py

Lines: 31-34, 57-108

Evidence:
  generate_id() (31-34): Importa uuid e retorna UUID, mas não é
  chamado em nenhum arquivo do projeto.
  process_task_data() (57-108): Função completa de validação de
  task data (51 linhas), nunca chamada em nenhum arquivo.

Impact:
  Código morto aumenta ruído cognitivo e carga de manutenção.

Recommendation:
  Remover ambas as funções. process_task_data() poderia ter sido
  aproveitada nas rotas para evitar duplicação — mas não foi.

Status: OPEN
```

---

### L2

```
ID: AP204

Severity: LOW

Title: Unused Service — NotificationService

File: services/notification_service.py

Lines: 1-49

Evidence:
  NotificationService nunca é importado por nenhum arquivo
  do projeto. Serviço com credenciais hardcoded (C1) que
  nunca é executado.

Impact:
  Serviço inutilizado. Credenciais hardcoded sem benefício.

Recommendation:
  Integrar ao fluxo de criação de tasks (notify_task_assigned)
  após resolver C1 (mover credenciais para env vars).

Status: OPEN
```

---

### L3

```
ID: AP204

Severity: LOW

Title: Unused Imports

Files:
  routes/task_routes.py: linha 7 — json, os, sys, time
  app.py: linha 7 — sys, json, datetime (parcial)

Evidence:
  import json, os, sys, time na task_routes.py — nenhum usado.
  sys e json em app.py — não usados no arquivo.

Impact:
  Ruído de importação. Potencial confusão sobre dependências reais.

Recommendation:
  Remover imports não utilizados.

Status: OPEN
```

---

## DEPRECATED APIS

| API | File | Lines | Reason | Replacement | Complexity |
|-----|------|-------|--------|-------------|------------|
| `Model.query.get(id)` | routes/user_routes.py | 29, 94, 136, 155 | Deprecado no SQLAlchemy 2.0 | `db.session.get(Model, id)` | Low |
| `Model.query.get(id)` | routes/task_routes.py | 67, 117, 122, 158, 188, 195 | Deprecado no SQLAlchemy 2.0 | `db.session.get(Model, id)` | Low |
| `Model.query.get(id)` | routes/report_routes.py | 105 | Deprecado no SQLAlchemy 2.0 | `db.session.get(Model, id)` | Low |
| `datetime.utcnow()` | múltiplos arquivos | vários | Deprecado no Python 3.12 | `datetime.now(timezone.utc)` | Low |

---

## MVC MIGRATION PLAN

| Field | Value |
|-------|-------|
| Selected Migration Strategy | Incremental Migration (Partial MVC → Full MVC) |
| Reason | Projeto já possui models/, routes/, services/, utils/. Adicionar controllers/ e emagrecer routes. |
| Planned Changes | Ver Passo a Passo abaixo |
| Expected Target Architecture | Flask MVC completo com config/, controllers/, services/, models/, routes/, utils/ |

### Passo a Passo

1. **Segurança** — `config/settings.py`, MD5→werkzeug, env vars
2. **Services** — `user_service.py`, `task_service.py`, `report_service.py`
3. **Controllers** — `user_controller.py`, `task_controller.py`, `report_controller.py`
4. **Routes** — emagrecer para apenas Blueprint + url_rule
5. **Performance** — joinedload no GET /tasks
6. **Limpeza** — dead code, unused imports

---

## RISK ASSESSMENT

| Risk Level | Changes |
|------------|---------|
| Low Risk | Criar config/settings.py, criar services/, criar controllers/ |
| Medium Risk | Modificar models/user.py (hash algorithm — migração de senhas existentes necessária) |
| High Risk | Emagrecer routes (risco de quebrar contratos de endpoint) |
| Potential Breaking Changes | Troca de MD5 → werkzeug invalida senhas existentes no banco (seed.py precisará ser re-executado ou senhas migradas) |

---

## REFACTORING CHECKLIST

- [ ] **Security**: Mover credenciais para .env
- [ ] **Security**: Substituir MD5 por werkzeug hash
- [ ] **Architecture**: Criar config/settings.py
- [ ] **Architecture**: Criar controllers/ com 3 arquivos
- [ ] **Architecture**: Criar services/user_service.py
- [ ] **Architecture**: Criar services/task_service.py
- [ ] **Architecture**: Criar services/report_service.py
- [ ] **Controllers**: Extrair lógica de user_routes.py
- [ ] **Controllers**: Extrair lógica de task_routes.py
- [ ] **Controllers**: Extrair lógica de report_routes.py
- [ ] **Routes**: Emagrecer user_routes.py → só Blueprint
- [ ] **Routes**: Emagrecer task_routes.py → só Blueprint
- [ ] **Routes**: Emagrecer report_routes.py → só Blueprint
- [ ] **Models**: Atualizar User.to_dict() para não expor password
- [ ] **Validation**: Centralizar em services usando constantes de helpers.py
- [ ] **Services**: Corrigir N+1 com joinedload
- [ ] **Configuration**: app.py importar config/settings.py

---

## VALIDATION PLAN

| Item | Method | Status |
|------|--------|--------|
| Boot Validation | `python app.py` sem erros | NOT VERIFIED |
| Endpoint Validation | Todos os 22 endpoints respondem corretamente | NOT VERIFIED |
| Architecture Validation | controllers/, services/, config/ presentes com responsabilidades corretas | NOT VERIFIED |
| Configuration Validation | Nenhum hardcoded secret no código | NOT VERIFIED |

---

## FINAL STATUS

| Field | Value |
|-------|-------|
| Findings Open | 2 (H1 — Fake JWT; L2 — NotificationService não integrado) |
| Findings Resolved | 13 |
| Migration Readiness | COMPLETE |

## POST-REFACTOR VALIDATION

| Item | Status |
|------|--------|
| Application Boot | PASS |
| GET /health | PASS |
| GET /users | PASS |
| POST /login (werkzeug hash) | PASS |
| GET /tasks (joinedload, sem N+1) | PASS |
| POST /tasks | PASS |
| GET /tasks/stats | PASS |
| GET /reports/summary | PASS |
| GET /categories | PASS |
| GET /users/1/tasks | PASS |
| GET /reports/user/1 | PASS |
| DELETE /tasks/1 | PASS |
| 404 para recurso inexistente | PASS |
| Nenhum MD5 no código | PASS |
| Nenhuma credencial hardcoded | PASS |
| is_overdue() centralizado (1 definição, 6 usos) | PASS |
| Routes finas (35 LOC total) | PASS |
| config/ com settings.py | PASS |
| controllers/ com 3 arquivos | PASS |
| services/ com 4 arquivos | PASS |
