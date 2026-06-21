# Safety Rules

## Purpose

Define mandatory safety constraints that must be respected during analysis, planning and refactoring.

These rules exist to prevent:

* functional regressions
* behavioral changes
* data loss
* architecture drift
* accidental rewrites
* unsupported assumptions

Safety rules override refactoring opportunities.

When a refactoring conflicts with a safety rule:

```text
Safety Rule Wins
```

---

# Core Principle

## Preserve Behavior

The primary objective of refactoring is:

```text
Improve Architecture
Without Changing Behavior
```

Business behavior must remain identical unless explicitly requested.

This includes:

* endpoint behavior
* response payloads
* validation rules
* business rules
* persistence behavior
* authentication behavior

---

# SR001 - No Functional Changes

Never introduce:

* new business rules
* modified business rules
* additional validations
* removed validations
* changed workflows

Forbidden:

Before:

```python
if customer.total > 1000:
    discount = 0.10
```

After:

```python
if customer.total > 500:
    discount = 0.10
```

Reason:

Behavior changed.

Allowed:

Move code without changing logic.

---

# SR002 - No Implicit Feature Additions

Never add:

* caching
* retries
* pagination
* authentication
* authorization
* logging features
* metrics collection

unless explicitly requested.

Forbidden:

```python
@cache
def get_user():
```

if caching did not exist before.

---

# SR003 - No Implicit Dependency Upgrades

Refactoring does not imply modernization.

Do not upgrade:

* frameworks
* libraries
* runtime versions

unless explicitly requested.

Forbidden:

```text
Flask 1.x → Flask 3.x
```

during architectural migration.

Allowed:

Maintain current dependency versions.

---

# SR004 - No Rewrite Strategy

Refactoring must not become a rewrite.

Prefer:

```text
Move
Extract
Split
Isolate
```

Avoid:

```text
Rewrite
Replace
Redesign
```

unless explicitly requested.

---

# SR005 - Preserve Public Contracts

Maintain:

* endpoint URLs
* HTTP methods
* request formats
* response formats
* response status codes

Forbidden:

Before:

```http
GET /users/1
```

After:

```http
GET /api/users/1
```

Reason:

Contract changed.

---

# SR006 - Preserve Database Schema

Do not modify:

* tables
* columns
* indexes
* constraints

unless explicitly requested.

Forbidden:

```sql
ALTER TABLE users
ADD COLUMN status
```

Reason:

Schema changed.

---

# SR007 - Preserve Persistence Behavior

Do not change:

* query semantics
* transaction boundaries
* save operations
* delete behavior

unless required to preserve existing functionality.

Forbidden:

Before:

```python
db.session.commit()
```

After:

```python
background_commit()
```

Reason:

Persistence behavior changed.

---

# SR008 - Preserve Authentication Behavior

Do not modify:

* login flows
* session management
* token behavior
* permission checks

unless explicitly requested.

Forbidden:

```python
if user.is_admin:
```

becoming:

```python
if user.role == "admin":
```

without validation.

---

# SR009 - Preserve Error Handling Semantics

Maintain:

* status codes
* error messages
* exception behavior

Forbidden:

Before:

```python
return {"error": "Not Found"}, 404
```

After:

```python
raise Exception()
```

Reason:

Contract changed.

---

# SR010 - No Assumption-Based Refactoring

Never refactor based on assumptions.

Evidence is required.

Forbidden:

```text
Folder is called service
therefore it contains business logic
```

Required:

Inspect implementation.

---

# SR011 - No Architecture Assumptions

Folder structure does not prove architecture.

Forbidden:

```text
controllers/
services/
models/
```

therefore:

```text
MVC
```

Required:

Verify implementation responsibilities.

---

# SR012 - Preserve Dependency Flow During Migration

Allowed target flow:

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Model
```

During migration, temporary states may exist.

However:

Do not introduce new violations.

Forbidden:

```text
Route
  ↓
Database
```

---

# SR013 - Refactor One Concern At A Time

Avoid combining:

* architecture migration
* dependency upgrades
* framework upgrades
* feature development

in the same change set.

Preferred:

Step 1:

```text
Architecture Refactoring
```

Step 2:

```text
Validation
```

Step 3:

```text
Modernization
```

---

# SR014 - Preserve Endpoint Inventory

Every endpoint discovered during analysis must remain available after migration.

Unless explicitly requested.

Validation required.

---

# SR015 - Preserve Business Logic Ownership

When moving logic:

Allowed:

```text
Controller
  ↓
Service
```

Forbidden:

```text
Controller
  ↓
Route
```

Reason:

Logic moved to incorrect layer.

---

# SR016 - No Silent Data Transformations

Do not introduce:

* automatic formatting
* automatic normalization
* automatic conversions

unless they already exist.

Forbidden:

Before:

```json
{
  "name": "John Doe"
}
```

After:

```json
{
  "name": "john doe"
}
```

Reason:

Behavior changed.

---

# SR017 - Preserve External Integrations

Do not modify:

* APIs
* queues
* webhooks
* external services

unless explicitly requested.

Forbidden:

Replacing:

```text
Stripe
```

with:

```text
PayPal
```

during refactoring.

---

# SR018 - Validate Before And After

Before refactoring:

Capture:

* endpoint inventory
* architecture inventory
* dependency inventory

After refactoring:

Verify:

* endpoints
* contracts
* startup behavior
* dependency flow

Behavioral parity is mandatory.

---

# SR019 - Refactoring Must Be Reversible

Refactoring steps should be:

* incremental
* isolated
* reviewable

Avoid large atomic rewrites.

Preferred:

```text
Small Change
Validate
Small Change
Validate
```

---

# SR020 - Evidence Required For Every Finding

Every recommendation must be traceable to:

* source code
* configuration
* dependency files
* audit findings

Forbidden:

```text
This project should use repositories.
```

without supporting evidence.

---

# Validation Checklist

Before approving a refactoring plan verify:

* no business rules changed
* no endpoints changed
* no response contracts changed
* no database schema changed
* no authentication behavior changed
* no external integrations changed
* no dependency upgrades performed
* no assumptions used as evidence

All checks must pass.

---

# Escalation Rules

If a proposed refactoring would:

* change behavior
* modify contracts
* alter persistence
* affect security

the plan must be flagged.

Status:

```text
REQUIRES_HUMAN_REVIEW
```

before execution.

---

# Final Rule

When uncertainty exists:

```text
Do Not Refactor
```

Investigate further.

Evidence always takes precedence over assumptions.

Preserving behavior always takes precedence over architectural improvement.