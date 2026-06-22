# Architecture Audit Report

---

## PROJECT INFORMATION

| Field             | Value                                                  |
|-------------------|--------------------------------------------------------|
| Project Name      | task-manager-api                                       |
| Analysis Date     | 2026-06-22                                             |
| Language          | Python                                                 |
| Framework         | Flask 3.0.0                                            |
| Database          | SQLite (sqlite:///tasks.db via DATABASE_URI env var)   |
| ORM               | Flask-SQLAlchemy 3.1.1                                 |
| Package Manager   | pip (requirements.txt)                                 |
| Architecture      | MVC + Service Layer (Route → Controller → Service → Model) |
| Domain            | Task Manager API — gerenciamento de tarefas com usuários, categorias e relatórios de produtividade |
| Confidence        | High                                                   |
| Files Analyzed    | 24 .py files                                           |
| Estimated LOC     | ~1 000 linhas                                          |

---

## PHASE 1 SUMMARY

| Check                     | Status  |
|---------------------------|---------|
| Stack Detection           | PASS    |
| Architecture Detection    | PASS    |
| Domain Detection          | PASS    |
| Endpoint Inventory        | PASS    |
| Anti-Pattern Analysis     | PASS    |
| Deprecated API Analysis   | PASS    |

Endpoints inventariados: 22

---

## FINDINGS

### Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 3     |
| MEDIUM   | 3     |
| LOW      | 4     |
| **Total**| **10**|

---

### [HIGH] AP400 — N+1 Query em ReportService.get_summary

**File:** `services/report_service.py:38–47`

**Evidence:**
```python
for u in User.query.all():           # carrega todos os usuários — 1 query
    user_tasks = Task.query.filter_by(user_id=u.id).all()  # +1 query por usuário
```

**Description:** O loop sobre usuários executa uma query de tasks por iteração. Com N usuários, são N+1 queries para um único endpoint.

**Impact:** Degradação de performance O(n). Para 1 000 usuários → 1 001 queries por chamada a `GET /reports/summary`.

**Recommendation:** Usar `joinedload(User.tasks)` no carregamento inicial para resolver em 1 query via JOIN.

---

### [HIGH] AP400 — N+1 Query em ReportService.get_categories

**File:** `services/report_service.py:128–130`

**Evidence:**
```python
for c in categories:
    cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()  # +1 query por categoria
```

**Description:** Para cada categoria, uma query de contagem é executada individualmente no banco.

**Impact:** O(n) queries por chamada a `GET /categories`. Cresce linearmente com o número de categorias.

**Recommendation:** Substituir pelo padrão de agregação com `db.func.count()` e `group_by`, resolvendo em 1 query.

---

### [HIGH] AP203 — Dead Code: notify_task_assigned Nunca Invocado

**File:** `services/task_service.py` (ausência de chamada) / `services/notification_service.py:26–35`

**Evidence:** `TaskService.create_task()` não contém nenhuma chamada a `NotificationService`. O método `notify_task_assigned()` está implementado mas nunca é acionado.

**Description:** A funcionalidade de notificação de atribuição de task existe no código mas está desconectada do fluxo de criação. É código morto com intenção declarada mas execução ausente.

**Impact:** Usuários atribuídos a tasks nunca recebem notificação. A feature consta como implementada mas é silenciosamente não-funcional.

**Recommendation:** Instanciar `NotificationService` em `TaskService` e chamar `notify_task_assigned(user, task)` em `create_task()` após commit, quando `user_id` é definido.

---

### [MEDIUM] AP600 — API Deprecated: datetime.utcnow()

**Files:**
- `models/task.py:15,16,52`
- `models/user.py:14`
- `models/category.py:11`
- `services/task_service.py:172`
- `services/report_service.py:27,30,31`
- `services/notification_service.py:35`

**Evidence:**
```python
# models/task.py:15
created_at = db.Column(db.DateTime, default=datetime.utcnow)
# services/task_service.py:172
task.updated_at = datetime.utcnow()
```

**Description:** `datetime.utcnow()` retorna objetos datetime sem timezone (naive). Foi marcado como deprecated no Python 3.12 e emite `DeprecationWarning` a partir desta versão.

**Impact:** Risco de compatibilidade com Python 3.12+. Comparações de datas tornam-se ambíguas. Possível remoção da API em versões futuras.

**Recommendation:** Substituir por `datetime.now(timezone.utc)` com `from datetime import timezone`. Padrão RP008 do playbook.

---

### [MEDIUM] AP200 — Ausência de Paginação

**Files:**
- `services/task_service.py:11–23` (`get_all_tasks`)
- `services/user_service.py:8–15` (`get_all_users`)
- `services/report_service.py:124–131` (`get_categories`)

**Evidence:**
```python
tasks = Task.query.options(...).all()   # retorna todos os registros
users = User.query.all()               # retorna todos os registros
```

**Description:** Os endpoints `GET /tasks`, `GET /users` e `GET /categories` retornam todos os registros sem paginação.

**Impact:** Tempo de resposta e uso de memória crescem linearmente com o volume de dados.

**Recommendation:** Adicionar parâmetros `page` e `per_page` e usar `.paginate()` do Flask-SQLAlchemy.

---

### [MEDIUM] AP301 — CORS Permissivo Sem Restrição de Origem

**File:** `app.py:16`

**Evidence:**
```python
CORS(app)  # permite qualquer origem
```

**Description:** A configuração `CORS(app)` sem parâmetros permite requisições cross-origin de qualquer domínio.

**Impact:** Qualquer site pode fazer requisições cross-origin à API em contexto de browser, facilitando ataques CSRF.

**Recommendation:** Restringir origens: `CORS(app, origins=['https://seu-frontend.com'])` ou ler de variável de ambiente.

---

### [LOW] AP700 — Política de Senha Fraca

**File:** `utils/helpers.py:43`

**Evidence:**
```python
MIN_PASSWORD_LENGTH = 4
```

**Description:** O mínimo de 4 caracteres para senhas é insuficiente para qualquer contexto de produção.

**Impact:** Senhas de 4 caracteres são trivialmente brute-forçadas.

**Recommendation:** Elevar para no mínimo 8 caracteres.

---

### [LOW] AP701 — Token JWT Simulado (Stub)

**File:** `controllers/user_controller.py:69`

**Evidence:**
```python
'token': 'fake-jwt-token-' + str(user.id)
```

**Description:** O endpoint de login retorna um token previsível e não assinado.

**Impact:** Ausência de autenticação real. O token pode ser forjado trivialmente.

**Recommendation:** Implementar JWT real com `PyJWT`.

---

### [LOW] AP702 — Import Não Utilizado

**File:** `models/task.py:3`

**Evidence:**
```python
import json  # nunca utilizado no arquivo
```

**Description:** Import sem uso.

**Recommendation:** Remover a linha.

---

### [LOW] AP300 — Valor Padrão DEBUG=true

**File:** `config/settings.py:8`

**Evidence:**
```python
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
```

**Description:** Se `DEBUG` env var não estiver definida, a aplicação inicia em modo debug, expondo o debugger do Werkzeug.

**Recommendation:** Alterar o padrão para `'false'`.

---

## ENDPOINT INVENTORY

| Method | Route                   | Controller                        | Response   |
|--------|-------------------------|-----------------------------------|------------|
| GET    | /tasks                  | task_controller.get_tasks         | JSON array |
| POST   | /tasks                  | task_controller.create_task       | JSON 201   |
| GET    | /tasks/search           | task_controller.search_tasks      | JSON array |
| GET    | /tasks/stats            | task_controller.task_stats        | JSON       |
| GET    | /tasks/<id>             | task_controller.get_task          | JSON       |
| PUT    | /tasks/<id>             | task_controller.update_task       | JSON       |
| DELETE | /tasks/<id>             | task_controller.delete_task       | JSON       |
| GET    | /users                  | user_controller.get_users         | JSON array |
| POST   | /users                  | user_controller.create_user       | JSON 201   |
| GET    | /users/<id>             | user_controller.get_user          | JSON       |
| PUT    | /users/<id>             | user_controller.update_user       | JSON       |
| DELETE | /users/<id>             | user_controller.delete_user       | JSON       |
| GET    | /users/<id>/tasks       | user_controller.get_user_tasks    | JSON array |
| POST   | /login                  | user_controller.login             | JSON       |
| GET    | /reports/summary        | report_controller.summary_report  | JSON       |
| GET    | /reports/user/<id>      | report_controller.user_report     | JSON       |
| GET    | /categories             | report_controller.get_categories  | JSON array |
| POST   | /categories             | report_controller.create_category | JSON 201   |
| PUT    | /categories/<id>        | report_controller.update_category | JSON       |
| DELETE | /categories/<id>        | report_controller.delete_category | JSON       |
| GET    | /health                 | health (inline app.py)            | JSON       |
| GET    | /                       | index (inline app.py)             | JSON       |
