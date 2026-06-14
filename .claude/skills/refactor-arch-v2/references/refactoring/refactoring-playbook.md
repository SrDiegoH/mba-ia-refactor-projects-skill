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