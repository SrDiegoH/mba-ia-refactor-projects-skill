# Project Migration Rules

## Purpose

Define how a project should be migrated based on the architecture detected during Phase 1.

Not all projects require the same migration strategy.

The migration effort must be proportional to the current architecture maturity.

The goal is to improve architecture while minimizing risk.

Always prefer incremental migration over unnecessary rewrites.

---

# Migration Principles

All migrations must follow these principles.

## Principle 1

Preserve behavior.

The application must continue to behave exactly as before.

---

## Principle 2

Preserve API contracts.

Do not change:

* routes
* HTTP methods
* request contracts
* response contracts
* authentication behavior

unless explicitly approved.

---

## Principle 3

Move code before rewriting code.

Preferred:

```text
Move existing logic into the correct layer.
```

Avoid:

```text
Rewrite working code unnecessarily.
```

---

## Principle 4

Minimize risk.

Favor small structural changes over large behavioral changes.

---

## Principle 5

Refactor only what is necessary.

Do not reorganize code that already follows MVC rules.

---

# Migration Strategy Selection

Choose the strategy based on the architecture classification produced by:

```text
architecture-detection.md
```

---

# MONOLITHIC

## Definition

Most responsibilities are concentrated in one or a few files.

Example:

```text
app.py
server.js
main.py
```

containing:

* routes
* business logic
* persistence
* configuration

---

## Strategy

FULL MVC MIGRATION

---

## Goals

Create:

```text
config/
controllers/
services/
models/
routes/
```

Extract responsibilities into their proper layers.

---

## Migration Order

1. Extract configuration
2. Extract models
3. Extract services
4. Extract controllers
5. Extract routes
6. Validate endpoints

---

## Example

Before:

```python
@app.route("/users")
def get_users():
    users = db.execute(...)
    return jsonify(users)
```

After:

```text
routes/
controllers/
services/
models/
```

with the same behavior preserved.

---

# PARTIAL_MVC

## Definition

Some MVC layers already exist.

Responsibilities are only partially separated.

---

## Examples

```text
models/
routes/
```

without services.

---

```text
services/
models/
```

but business logic still exists in controllers.

---

## Strategy

INCREMENTAL MVC MIGRATION

---

## Goals

Complete missing layers.

Move misplaced responsibilities.

Preserve existing structure whenever possible.

---

## Allowed Changes

✓ Move logic

✓ Create missing folders

✓ Split oversized files

---

## Avoid

✗ Reorganizing the entire project

✗ Renaming stable modules unnecessarily

✗ Rewriting working business logic

---

# MVC

## Definition

Project already follows MVC structure.

---

## Strategy

TARGETED IMPROVEMENTS

---

## Goals

Fix only:

* anti-patterns
* architectural violations
* deprecated APIs
* excessive coupling

---

## Avoid

✗ Full project restructuring

✗ Folder reorganization

✗ Large file moves

---

## Example

Bad:

```text
Rebuild entire project structure
```

Good:

```text
Move business logic from controller to service
```

---

# LAYERED

## Definition

Application uses technical layers instead of MVC.

Example:

```text
presentation/
application/
domain/
infrastructure/
```

---

## Strategy

LAYER MAPPING

---

## Goals

Map existing layers to MVC responsibilities.

Preserve existing architecture when possible.

---

## Example

```text
presentation/
```

maps to:

```text
routes/
controllers/
```

---

```text
application/
```

maps to:

```text
services/
```

---

```text
infrastructure/
```

maps to:

```text
models/
config/
```

---

## Avoid

✗ Destroying a well-structured layered architecture

✗ Rebuilding everything as MVC folders

---

# FEATURE_BASED

## Definition

Project organized by business domains.

Example:

```text
users/
orders/
payments/
```

Each feature contains:

* routes
* services
* models

---

## Strategy

FEATURE-PRESERVING MIGRATION

---

## Goals

Preserve feature boundaries.

Improve responsibility separation inside each feature.

---

## Example

Good:

```text
users/
├── routes/
├── controllers/
├── services/
└── models/
```

Bad:

```text
controllers/
models/
services/
```

moving every feature into global folders.

---

## Rule

Feature boundaries take precedence over MVC folder purity.

---

# MIXED

## Definition

Multiple architectural styles coexist.

Examples:

```text
controllers/
models/
```

plus

```text
users/
orders/
```

or

Some modules are monolithic while others are MVC.

---

## Strategy

NORMALIZATION FIRST

---

## Goals

Identify dominant architecture.

Normalize inconsistent modules.

Then migrate incrementally.

---

## Migration Order

1. Identify dominant pattern
2. Normalize outliers
3. Apply MVC rules
4. Validate

---

# UNKNOWN

## Definition

Architecture cannot be determined confidently.

---

## Strategy

CONSERVATIVE MIGRATION

---

## Goals

Apply only obvious improvements.

Avoid structural changes.

---

## Allowed Changes

✓ Configuration extraction

✓ Deprecated API replacement

✓ Small anti-pattern fixes

---

## Avoid

✗ Large-scale restructuring

✗ Folder migrations

✗ Aggressive code movement

---

# File Splitting Rules

Large files should be reviewed.

---

## Controllers

Recommended:

```text
< 100 lines
```

Review:

```text
> 200 lines
```

---

## Services

Recommended:

```text
< 300 lines
```

Review:

```text
> 500 lines
```

---

## Models

Recommended:

```text
One primary entity per file
```

---

# Folder Creation Rules

Create a folder only if it has a clear purpose.

Bad:

```text
services/
```

containing:

```text
__init__.py
```

only.

---

Good:

```text
services/
user_service.py
order_service.py
```

---

# Rename Rules

Avoid renaming stable files.

Only rename when:

* name is misleading
* architecture requires it
* user approved it

---

# Dependency Migration Rules

Preserve dependency direction.

Allowed:

```text
Route
 ↓
Controller
 ↓
Service
 ↓
Model
```

Forbidden:

```text
Model
 ↓
Controller
```

---

# Validation Requirement

Every migration must pass:

* endpoint validation
* architecture validation
* boot validation

before completion.

---

# Migration Decision Output

Before starting Phase 3, always produce:

```text
Migration Strategy: INCREMENTAL MVC MIGRATION

Architecture: PARTIAL_MVC

Reason:

- routes layer exists
- models layer exists
- business logic found in controllers

Planned Changes:

1. Create services layer
2. Move business rules
3. Preserve existing routes
```

This output must be generated before modifying files.

---

# Final Rule

The best migration is the smallest migration that achieves MVC compliance while preserving behavior.

Do not optimize for architectural perfection.

Optimize for correctness, maintainability and safety.