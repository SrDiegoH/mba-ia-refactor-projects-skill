# Architecture Validation

## Purpose

Define the validation process used to verify that a refactoring successfully achieved the intended architectural improvements.

Architecture validation occurs after refactoring and before modernization.

The objective is to verify:

* target architecture was achieved
* dependency flow is correct
* layer responsibilities are respected
* architectural violations were removed
* no new violations were introduced

Architecture validation is independent from functional validation.

Both are required.

---

# Validation Principles

## Validate Implementation

Validation must be based on implementation.

Never validate architecture using:

* folder names
* file names
* directory structure

Incorrect:

```text
controllers/
services/
models/
```

therefore:

```text
MVC
```

Correct:

Inspect responsibilities implemented in code.

---

## Validate Responsibilities

Architecture is determined by behavior.

Validation must confirm:

* routes handle routing
* controllers orchestrate requests
* services contain business logic
* models handle persistence

---

## Validate Dependency Flow

Validation must verify actual dependency relationships.

Folder organization alone is insufficient evidence.

---

# Target MVC Architecture

Expected dependency flow:

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Model
```

---

# Allowed Dependencies

Routes may depend on:

```text
Controller
```

Controllers may depend on:

```text
Service
```

Services may depend on:

```text
Model
```

Models should not depend on:

```text
Controller
Route
```

---

# Forbidden Dependencies

The following relationships are violations.

```text
Route → Model
```

```text
Route → Database
```

```text
Route → ORM
```

```text
Controller → Database
```

```text
Controller → ORM
```

```text
Model → Controller
```

```text
Model → Route
```

```text
Service → Route
```

```text
Service → Controller
```

---

# Validation Workflow

## Step 1 - Reclassify Architecture

Execute architecture detection again.

Reference:

```text
architecture-detection.md
```

Verify:

* architecture classification
* confidence level
* supporting evidence

Expected outcome:

```text
MVC
```

or

```text
MVC_WITH_SERVICES
```

depending on project rules.

---

## Step 2 - Rebuild Dependency Graph

Analyze imports and dependencies.

Build actual dependency graph.

Example:

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Model
```

Verify dependency direction.

---

## Step 3 - Reevaluate Findings

Re-run:

* anti-pattern detection
* dependency flow validation
* architecture analysis

Verify previously reported findings.

Expected:

```text
AP100 resolved
AP101 resolved
AP102 resolved
...
```

when applicable.

---

## Step 4 - Search For New Violations

Refactoring must not introduce:

* new anti-patterns
* new coupling
* new dependency cycles

Every migration can create new violations.

Validation must detect them.

---

# Layer Validation Rules

## Route Validation

Routes should:

* register endpoints
* map HTTP methods
* delegate execution

Routes should not:

* execute SQL
* access ORM
* implement business rules
* perform calculations

---

### Compliant Example

```python
@app.route("/users/<id>")
def get_user(id):
    return user_controller.get_user(id)
```

---

### Non-Compliant Example

```python
@app.route("/users/<id>")
def get_user(id):
    user = User.query.get(id)

    if user.total > 1000:
        discount = 0.20

    return {
        "discount": discount
    }
```

Finding:

```text
AP100
```

---

# Controller Validation

Controllers should:

* receive requests
* invoke services
* return responses

Controllers should not:

* implement business rules
* access ORM directly
* execute SQL
* contain workflow logic

---

### Compliant Example

```python
def get_user(id):
    return user_service.get_user(id)
```

---

### Non-Compliant Example

```python
def get_user(id):
    user = User.query.get(id)

    if user.total > 1000:
        discount = 0.20

    return {
        "discount": discount
    }
```

Findings:

```text
AP101
AP102
```

---

# Service Validation

Services should:

* contain business rules
* contain workflows
* coordinate persistence

Services should not:

* expose HTTP routes
* manipulate framework routing
* implement UI concerns

---

### Compliant Example

```python
def calculate_discount(user):
    if user.total > 1000:
        return 0.20

    return 0.10
```

---

# Model Validation

Models should:

* represent persistence
* define entities
* define database mappings

Models should not:

* call controllers
* expose routes
* implement presentation concerns

---

### Compliant Example

```python
class User(db.Model):
    pass
```

---

### Non-Compliant Example

```python
class User(db.Model):

    def get_response(self):
        return jsonify(...)
```

Potential Finding:

```text
AP105
```

---

# Dependency Validation Rules

## Rule DV001

Verify:

```text
Route → Controller
```

Allowed.

---

## Rule DV002

Verify:

```text
Controller → Service
```

Allowed.

---

## Rule DV003

Verify:

```text
Service → Model
```

Allowed.

---

## Rule DV004

Verify:

```text
Controller → Model
```

Not allowed.

Potential Finding:

```text
AP102
```

---

## Rule DV005

Verify:

```text
Route → Model
```

Not allowed.

Potential Finding:

```text
AP105
```

---

## Rule DV006

Verify:

```text
Circular Dependencies
```

Not allowed.

Potential Finding:

```text
AP106
```

---

# Resolution Validation

Every finding reported during audit must be reviewed.

Possible statuses:

---

## RESOLVED

Evidence no longer exists.

Example:

Before:

```python
user = User.query.get(id)
```

Controller contained ORM access.

After:

```python
return user_service.get_user(id)
```

Violation removed.

---

## PARTIALLY_RESOLVED

Violation reduced but still exists.

Example:

Business logic reduced but not fully removed.

---

## NOT_RESOLVED

Evidence still exists.

Original finding remains valid.

---

## REGRESSION

Refactoring introduced a new violation.

Immediate review required.

---

# Validation Report Format

For each validated finding:

```text
Finding:
AP101

Status:
RESOLVED

Evidence:
Business logic moved to service layer.

Validated File:
controllers/user_controller.py
```

---

# Architecture Completion Criteria

Architecture migration is considered complete when:

* no CRITICAL findings remain
* no HIGH findings remain
* dependency flow is compliant
* target architecture is achieved
* no regressions exist

---

# Migration Readiness Rules

## READY

Conditions:

```text
Target architecture achieved
No CRITICAL findings
No HIGH findings
No regressions
```

---

## REQUIRES_REVIEW

Conditions:

```text
High findings remain
Partial migration detected
```

---

## NOT_READY

Conditions:

```text
Critical findings remain
Dependency violations remain
Architecture incomplete
```

---

# Escalation Rules

If validation discovers:

* changed business rules
* changed endpoint contracts
* changed authentication behavior
* changed persistence behavior

stop validation.

Status:

```text
REQUIRES_HUMAN_REVIEW
```

Reference:

```text
safety-rules.md
```

---

# Final Rule

Architecture validation is successful only when:

1. target architecture is achieved
2. previous violations are resolved
3. no regressions exist
4. behavioral parity is preserved

Architectural improvement without behavioral preservation is considered a failed migration.