# Architecture Detection

## Purpose

Determine the current architecture of the project before performing any audit or refactoring.

The goal is not to identify the ideal architecture.

The goal is to identify the architecture that currently exists.

Always analyze the actual code structure before making assumptions.

Never assume MVC based solely on folder names.

Use evidence from source code.

---

# Detection Process

Execute the following steps in order.

## Step 1 - Identify Project Structure

Inspect:

* directory structure
* entry points
* routing files
* controllers
* services
* models
* repositories
* middleware
* utilities

Build a structural inventory.

Example:

```text
src/
├── app.py
├── routes/
├── services/
├── models/
└── database.py
```

---

## Step 2 - Identify Layer Separation

Determine whether the following responsibilities are separated.

### Routing

Examples:

* Flask routes
* Express routes
* FastAPI routers

### Controllers

Examples:

* request handling
* orchestration
* response generation

### Services

Examples:

* business rules
* use cases
* workflow logic

### Persistence

Examples:

* SQL
* ORM
* repositories

### Configuration

Examples:

* environment variables
* settings files
* configuration modules

---

## Step 3 - Classify Architecture

Choose the best matching architecture.

Only one classification should be selected.

---

# Architecture Types

## MONOLITHIC

### Description

Most responsibilities are concentrated in a small number of files.

### Indicators

Routing, business logic and persistence mixed together.

Examples:

```python
@app.route("/users")
def get_users():
    conn.execute(...)
    validate(...)
    calculate(...)
```

or

```javascript
app.get("/users", async (req, res) => {
    db.query(...)
    processOrder(...)
    sendResponse(...)
})
```

### Strong Signals

* Single file > 300 lines
* Multiple domains in same file
* SQL mixed with routes
* Business logic mixed with controllers

### Classification

MONOLITHIC

---

## PARTIAL MVC

### Description

Some MVC layers exist but separation is incomplete.

### Indicators

Project contains:

```text
models/
routes/
services/
```

but controllers still contain business logic.

Or:

```text
routes/
models/
```

without services.

### Strong Signals

* Partial layer separation
* Mixed responsibilities
* Some business logic still inside routes/controllers

### Classification

PARTIAL_MVC

---

## MVC

### Description

Responsibilities are separated into distinct layers.

### Indicators

```text
controllers/
models/
routes/
services/
config/
```

Controllers orchestrate.

Services contain business logic.

Models contain persistence logic.

Routes register endpoints.

### Strong Signals

* Clear layer boundaries
* Minimal cross-layer leakage
* Configuration isolated

### Classification

MVC

---

## LAYERED

### Description

Application organized by technical layers.

### Example

```text
presentation/
application/
domain/
infrastructure/
```

or

```text
api/
service/
repository/
database/
```

### Strong Signals

* Clear layer separation
* Business logic outside controllers
* Persistence isolated

### Classification

LAYERED

---

## FEATURE_BASED

### Description

Project organized by business domain.

### Example

```text
users/
orders/
payments/
```

Each feature contains its own routes, services and models.

### Strong Signals

* Feature folders
* Domain-oriented organization

### Classification

FEATURE_BASED

---

## MIXED

### Description

Multiple architectural styles coexist.

### Example

```text
controllers/
models/

users/
orders/
```

or

Some modules are MVC while others are monolithic.

### Classification

MIXED

---

## UNKNOWN

### Description

Architecture cannot be determined with reasonable confidence.

### Classification

UNKNOWN

---

# Confidence Score

Provide a confidence level.

## HIGH

Clear evidence.

Examples:

* consistent structure
* clear separation
* obvious architectural pattern

---

## MEDIUM

Partial evidence.

Examples:

* some expected folders missing
* mixed conventions

---

## LOW

Weak evidence.

Examples:

* very small project
* unconventional structure
* insufficient information

---

# Architecture Smell Indicators

The following findings do not determine architecture alone but should influence confidence.

## Indicators

* God Classes
* Large Controllers
* SQL in Routes
* Global State
* Duplicate Logic
* Mixed Domains
* Hardcoded Configuration

---

# Architecture Detection Output

Always produce the following format.

```text
Architecture: MONOLITHIC

Confidence: HIGH

Evidence:

- app.py contains routing, SQL and business rules
- No service layer found
- No controller layer found
- Configuration mixed with application logic
```

---

# Detection Rules

Always prefer evidence over naming.

Do not classify MVC only because folders named "controllers" or "models" exist.

Verify actual responsibilities.

Folder names alone are insufficient.

Analyze implementation.

---

# Migration Guidance

This classification will be used by the refactoring phase.

## MONOLITHIC

Perform full MVC migration.

## PARTIAL_MVC

Perform incremental MVC migration.

## MVC

Perform targeted improvements only.

## LAYERED

Map layers to MVC responsibilities without unnecessary rewrites.

## FEATURE_BASED

Preserve feature boundaries whenever possible.

## MIXED

Normalize architecture before MVC migration.

## UNKNOWN

Use conservative incremental changes.

```
```