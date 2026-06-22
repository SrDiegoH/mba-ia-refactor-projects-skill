# Refactoring Playbook

## Purpose

Define the mandatory refactoring workflow used during migration.

This playbook ensures that architectural improvements are:

* safe
* incremental
* verifiable
* reversible

The objective is not to rewrite the application.

The objective is to improve architecture while preserving behavior.

---

# Core Principles

## Preserve Behavior

The application must behave exactly the same before and after refactoring.

Architectural improvements must not introduce functional changes.

Business rules must remain unchanged.

---

## Small Incremental Changes

Prefer:

```text
Small refactorings
+
Validation
+
Small refactorings
+
Validation
```

Avoid:

```text
Large rewrites
```

---

## Evidence-Based Refactoring

Every refactoring action must be justified by:

* audit findings
* architectural violations
* maintainability concerns
* dependency issues

Never refactor based solely on personal preference.

---

## Refactor Before Rewrite

Prefer:

```text
Extract
Move
Isolate
Simplify
```

Avoid:

```text
Rewrite from scratch
```

unless explicitly requested.

---

# Refactoring Workflow

## Phase 1 - Audit

Perform complete analysis.

Required outputs:

* architecture classification
* endpoint inventory
* dependency inventory
* anti-pattern findings
* migration complexity

References:

```text
references/analysis/
references/audit/
```

---

## Phase 2 - Planning

Create migration plan.

The plan must include:

* target architecture
* impacted files
* migration order
* risks
* validation strategy

Do not modify code yet.

---

## Phase 3 - Structural Refactoring

Refactor architecture.

Focus on:

* layer separation
* dependency flow
* code organization

Do not introduce new functionality.

---

## Phase 4 - Validation

Verify:

* application behavior
* endpoint contracts
* dependency flow
* startup behavior

Behavioral parity is mandatory.

---

## Phase 5 - Modernization

Only after architecture is stable.

Examples:

* deprecated API migration
* dependency upgrades
* framework modernization

---

# Refactoring Order

Always apply refactorings in the following order.

---

## Step 1

Resolve:

```text
CRITICAL
```

findings.

Reference:

```text
severity-matrix.md
```

---

## Step 2

Resolve:

```text
HIGH
```

findings.

---

## Step 3

Resolve:

```text
MEDIUM
```

findings.

---

## Step 4

Resolve:

```text
LOW
```

findings if beneficial.

---

# MVC Migration Strategy

Target dependency flow:

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Model
```

Allowed dependencies:

```text
Route → Controller

Controller → Service

Service → Model
```

Forbidden dependencies:

```text
Route → Model

Route → Database

Controller → Database

Model → Controller

Model → Route
```

---

# Refactoring Patterns

## RP001 - Extract Service

Use when:

* controller contains business logic
* route contains business logic

Before:

```python
@app.route("/users/<id>")
def get_user(id):
    user = User.query.get(id)

    if user.total > 1000:
        discount = 0.20
    else:
        discount = 0.10

    return {
        "discount": discount
    }
```

After:

```python
@app.route("/users/<id>")
def get_user(id):
    return user_service.get_user(id)
```

```python
def get_user(id):
    user = User.query.get(id)

    if user.total > 1000:
        discount = 0.20
    else:
        discount = 0.10

    return {
        "discount": discount
    }
```

Applicable Findings:

```text
AP100
AP101
```

---

## RP002 - Move Database Access

Use when:

* controllers access ORM directly
* controllers execute SQL directly

Before:

```python
user = User.query.get(id)
```

After:

```python
user_service.get_user(id)
```

Applicable Findings:

```text
AP102
AP103
```

---

## RP003 - Introduce Service Layer

Use when:

* business logic exists
* no service layer exists

Before:

```text
Route → Controller → Model
```

After:

```text
Route → Controller → Service → Model
```

Applicable Findings:

```text
AP104
```

---

## RP004 - Break Circular Dependency

Use when:

```text
A → B
B → A
```

is detected.

Strategies:

* extract shared abstraction
* introduce service layer
* invert dependency direction

Applicable Findings:

```text
AP106
```

---

## RP005 - Extract Reusable Logic

Use when:

* duplicate code exists
* common workflows exist

Before:

```python
calculate_discount()
```

appears multiple times.

After:

```python
discount_service.calculate()
```

Applicable Findings:

```text
AP203
```

---

## RP006 - Secure Password Hashing

Use when:

* passwords are stored as plaintext
* passwords are hashed with MD5 or SHA1 (no salt)
* passwords are encoded with Base64 (reversible — not a hash)
* any custom "encryption" loop that does not use a proper KDF

Before (Python — MD5 without salt):

```python
import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_password(stored, provided):
    return stored == hashlib.md5(provided.encode()).hexdigest()
```

After (Python — werkzeug PBKDF2):

```python
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(stored_hash, provided):
    return check_password_hash(stored_hash, provided)
```

Before (Node.js — Base64 accumulation loop):

```javascript
function badCrypto(password) {
    let result = password;
    for (let i = 0; i < 10000; i++) {
        result = Buffer.from(result).toString('base64');
    }
    return result.slice(0, 32);
}
```

After (Node.js — bcrypt):

```javascript
const bcrypt = require('bcrypt');

async function hashPassword(password) {
    return bcrypt.hash(password, 12);
}

async function verifyPassword(plaintext, hash) {
    return bcrypt.compare(plaintext, hash);
}
```

Applicable Findings:

```text
AP003
AP001
```

---

## RP007 - Remove or Protect Dangerous Endpoint

Use when:

* an endpoint executes arbitrary SQL received from the request body
* an admin endpoint has no authentication or authorization check
* an endpoint exposes sensitive runtime data (SECRET_KEY, DB credentials, debug info)
* a utility/debug route is reachable without credentials in a non-development environment

Before (Python — raw SQL execution endpoint without auth):

```python
@app.route("/admin/query", methods=["POST"])
def exec_query():
    sql = request.json.get("sql")
    cursor = db.execute(sql)          # arbitrary SQL injection vector
    return jsonify(cursor.fetchall())

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "secret_key": app.config["SECRET_KEY"],   # exposes secret
        "debug": app.config["DEBUG"]
    })
```

After (Python — endpoint removed or properly guarded):

```python
# /admin/query removed entirely — no legitimate production use case.

@app.route("/health")
def health():
    return jsonify({"status": "ok"})  # no sensitive data exposed
```

Before (Node.js — financial report without auth):

```javascript
app.get('/api/admin/financial-report', (req, res) => {
    // no authentication check
    generateReport(res);
});
```

After (Node.js — protected with auth middleware):

```javascript
const { requireAdmin } = require('../middleware/auth');

router.get('/api/admin/financial-report', requireAdmin, financialController.getReport);
```

Applicable Findings:

```text
AP001
AP002
AP004
```

---

## RP008 - Replace Deprecated API

Use when:

* the codebase uses language or framework APIs that are marked deprecated in the current runtime version
* a library function has a known secure replacement (e.g. insecure cipher constructors)

Before (Python — datetime.utcnow() deprecated since 3.12):

```python
from datetime import datetime

created_at = datetime.utcnow()
```

After (Python — timezone-aware):

```python
from datetime import datetime, timezone

created_at = datetime.now(timezone.utc)
```

Before (Node.js — crypto.createCipher deprecated since v10):

```javascript
const cipher = crypto.createCipher('aes-256-cbc', key);
```

After (Node.js — explicit IV required):

```javascript
const iv = crypto.randomBytes(16);
const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
```

Before (Flask-SQLAlchemy — SQLALCHEMY_DATABASE_URI set directly on app.config without init_app pattern):

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)   # tight coupling, deprecated pattern
```

After (Flask-SQLAlchemy — application factory with init_app):

```python
# database.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# app.py
from database import db
def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db.init_app(app)
    return app
```

Applicable Findings:

```text
AP600
AP601
AP700
```