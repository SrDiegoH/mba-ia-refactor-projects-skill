# MVC Rules

## Purpose

Define the target MVC architecture.

This document describes the responsibilities and boundaries of each layer.

The objective is not merely to create MVC folders.

The objective is to create clear separation of concerns.

All refactoring decisions must follow these rules.

When a conflict exists between current implementation and these rules, prefer the MVC rules.

---

# MVC Principles

The architecture must separate:

* Presentation
* Request Handling
* Business Logic
* Persistence
* Configuration

Each responsibility must exist in exactly one layer.

Avoid duplicated responsibilities.

---

# Target Architecture

```text
src/
├── config/
├── controllers/
├── services/
├── models/
├── routes/
├── middleware/
├── utils/
└── app
```

Folders may vary by framework.

Responsibilities must remain consistent.

---

# Layer Definitions

## Routes Layer

### Purpose

Register application endpoints.

Map HTTP requests to controllers.

---

### Allowed Responsibilities

* Route registration
* URL definitions
* Middleware registration
* Controller binding

Examples:

Python

```python
bp.route("/users")(UserController.get_users)
```

Node

```javascript
router.get("/users", UserController.getUsers)
```

---

### Forbidden Responsibilities

* Business logic
* SQL queries
* ORM operations
* Validation rules
* Domain calculations

Bad Example

```python
@bp.route("/users")
def get_users():
    users = db.execute(...)
```

Reason:

Persistence logic inside route.

---

### Output

Routes should delegate immediately.

Good Example

```python
@bp.route("/users")
def get_users():
    return UserController.get_users()
```

---

# Controllers Layer

## Purpose

Receive requests and coordinate execution.

Controllers act as orchestration layers.

---

## Allowed Responsibilities

* Read request data
* Invoke services
* Return responses
* Translate exceptions
* Map DTOs

Examples:

```python
user = UserService.get_user(id)
return jsonify(user)
```

---

## Forbidden Responsibilities

* Complex business rules
* SQL queries
* ORM queries
* File persistence
* Domain calculations

Bad Example

```python
if order.total > 1000:
    apply_discount()
```

Reason:

Business logic belongs to service layer.

---

## Controller Rule

Controllers should be thin.

Preferred size:

```text
< 100 lines
```

Controllers larger than:

```text
200 lines
```

should be flagged for review.

---

# Services Layer

## Purpose

Contain business logic.

This is the heart of the application.

---

## Allowed Responsibilities

* Business rules
* Use cases
* Workflow execution
* Domain calculations
* Cross-entity operations
* Transaction orchestration

Examples:

```python
calculate_discount()
process_order()
assign_task()
close_project()
```

---

## Forbidden Responsibilities

* Route registration
* Direct HTTP handling
* Response formatting

Avoid:

```python
jsonify(...)
res.send(...)
```

inside services.

---

## Service Rule

Business decisions belong here.

Examples:

Good

```python
if customer.is_premium:
    discount = 0.2
```

Bad

```python
if customer.is_premium:
    return jsonify(...)
```

---

# Models Layer

## Purpose

Represent domain entities and persistence structures.

---

## Allowed Responsibilities

* ORM models
* Entity definitions
* Data mapping
* Repository access
* Database interaction

Examples:

```python
class User(db.Model):
```

```javascript
sequelize.define(...)
```

---

## Forbidden Responsibilities

* HTTP handling
* Route registration
* Response generation
* Workflow orchestration

---

## Model Rule

Models describe data.

Services describe behavior.

---

# Configuration Layer

## Purpose

Centralize application configuration.

---

## Allowed Responsibilities

* Environment variables
* Secrets loading
* Database configuration
* Logging configuration
* Application settings

Examples:

```python
DATABASE_URL
SECRET_KEY
REDIS_URL
```

---

## Forbidden Responsibilities

* Business rules
* Controllers
* Services

---

## Configuration Rule

No hardcoded credentials.

Bad

```python
SECRET_KEY = "abc123"
```

Good

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

---

# Middleware Layer

## Purpose

Execute logic before or after requests.

---

## Allowed Responsibilities

* Authentication
* Authorization
* Logging
* Rate limiting
* Request tracing

---

## Forbidden Responsibilities

* Business workflows
* Persistence
* Domain calculations

---

# Utilities Layer

## Purpose

Provide reusable technical helpers.

---

## Allowed Responsibilities

* Date formatting
* String helpers
* Serialization
* Parsing

---

## Forbidden Responsibilities

* Business rules
* Persistence
* Request handling

---

# Dependency Direction

Dependencies must flow downward.

```text
Routes
 ↓
Controllers
 ↓
Services
 ↓
Models
```

---

Allowed:

```text
Controller -> Service
```

Allowed:

```text
Service -> Model
```

Forbidden:

```text
Model -> Controller
```

Forbidden:

```text
Service -> Route
```

Forbidden:

```text
Route -> Model
```

---

# Validation Placement

Validation responsibilities:

Simple request validation:

```text
Controller
```

Business validation:

```text
Service
```

Database constraints:

```text
Model
```

---

# Error Handling

Controllers may translate exceptions.

Business exceptions should originate from services.

Persistence exceptions should originate from models.

Example:

```text
Model
  ↓
Service
  ↓
Controller
```

---

# Anti-Patterns

The following must be reported.

---

## Business Logic In Controller

Severity:

HIGH

Example:

```python
if total > 1000:
    apply_discount()
```

---

## SQL In Route

Severity:

HIGH

Example:

```python
@route(...)
db.execute(...)
```

---

## Controller Accessing Database Directly

Severity:

HIGH

Example:

```python
User.query.all()
```

inside controller.

---

## Fat Controller

Severity:

MEDIUM

Condition:

```text
> 200 lines
```

---

## God Service

Severity:

MEDIUM

Condition:

```text
> 500 lines
```

or

Multiple unrelated responsibilities.

---

# Migration Rules

When refactoring:

1. Preserve behavior.
2. Preserve endpoint contracts.
3. Preserve response formats.
4. Preserve authentication behavior.
5. Prefer moving code over rewriting code.

---

# Validation Checklist

MVC compliance requires:

✓ Routes only register endpoints

✓ Controllers only orchestrate

✓ Services contain business logic

✓ Models contain persistence logic

✓ Configuration centralized

✓ Dependency direction respected

✓ No SQL in routes

✓ No business rules in controllers

✓ No HTTP responses in services

---

# Final Rule

MVC compliance is determined by responsibilities.

Folder names alone do not make a project MVC.

Always evaluate actual implementation.