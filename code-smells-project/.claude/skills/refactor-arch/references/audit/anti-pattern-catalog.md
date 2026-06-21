# Anti-Pattern Catalog

## Purpose

Define all architectural, maintainability, security, configuration and code-quality anti-patterns that should be detected during Phase 2.

Each anti-pattern must be reported using:

* ID
* Severity
* Detection Criteria
* Impact
* Recommendation

Detection must be evidence-based.

Never report findings without supporting evidence.

---

# Severity Assignment

Severity classification is defined in:

```text
severity-matrix.md
```

This document assigns severity levels to anti-patterns.

Severity definitions must not be duplicated here.

---

# Detection Principles

Anti-pattern detection must be based on implementation evidence.

Do not infer violations solely from:

* folder names
* file names
* project structure
* architectural assumptions

Implementation evidence is mandatory.

---

# SECURITY

## AP001 - Hardcoded Credentials

Severity:

```text
CRITICAL
```

(See severity-matrix.md)

Detection:

* API keys in source code
* passwords in source code
* tokens in source code
* secrets committed to repository

Examples:

```python
API_KEY = "123456"
```

```javascript
const TOKEN = "abcdef"
```

Impact:

Credential exposure.

Recommendation:

Move secrets to environment variables.

---

## AP002 - SQL Injection Risk

Severity:

```text
CRITICAL
```

(See severity-matrix.md)

Detection:

SQL built using string concatenation or interpolation with user-controlled data.

Example:

```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

Impact:

Unauthorized database access.

Recommendation:

Use parameterized queries.

---

## AP003 - Command Injection Risk

Severity:

```text
CRITICAL
```

(See severity-matrix.md)

Detection:

User-controlled input passed to shell execution.

Examples:

```python
os.system(user_input)
```

```javascript
exec(req.body.command)
```

Impact:

Remote code execution.

Recommendation:

Avoid shell execution or sanitize inputs.

---

## AP004 - Insecure Deserialization

Severity:

```text
CRITICAL
```

(See severity-matrix.md)

Detection:

Unsafe deserialization of untrusted data.

Examples:

```python
pickle.loads(data)
```

Impact:

Arbitrary code execution.

Recommendation:

Use safe serialization formats.

---

# ARCHITECTURE

## AP100 - Business Logic In Route

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Route contains business decisions, calculations or workflows.

Impact:

Violates separation of concerns.

Recommendation:

Move logic to service layer.

---

## AP101 - Business Logic In Controller

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Controller performs domain decisions or business workflows.

Impact:

Fat controllers.

Recommendation:

Move business rules to services.

---

## AP102 - Direct Database Access In Controller

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

ORM queries or SQL executed directly in controller code.

Impact:

Tight coupling.

Recommendation:

Move persistence access to model or repository layer.

---

## AP103 - SQL In Route

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Routes execute SQL directly.

Impact:

Architectural violation.

Recommendation:

Move persistence logic to model or repository layer.

---

## AP104 - Missing Service Layer

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Business logic exists but no service layer is present.

Impact:

Reduced maintainability.

Recommendation:

Introduce service layer.

---

## AP105 - Layer Bypass

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Dependency flow bypasses MVC layers.

Examples:

```text
Route → Model
Controller → Database
```

Impact:

Architectural inconsistency.

Recommendation:

Restore dependency flow.

---

## AP106 - Circular Dependency

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Module A depends on Module B and Module B depends on Module A.

Impact:

Fragile architecture.

Recommendation:

Break dependency chain.

---

# MAINTAINABILITY

## AP200 - God Class

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection Signals:

* multiple unrelated responsibilities
* excessive size
* excessive dependencies

Typical indicators:

* > 500 lines
* multiple domains handled
* mixed responsibilities

Impact:

Difficult maintenance.

Recommendation:

Split responsibilities.

---

## AP201 - Fat Controller

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Controller exceeds recommended complexity.

Typical indicators:

* > 200 lines
* multiple responsibilities

Impact:

Reduced readability.

Recommendation:

Move logic to services.

---

## AP202 - Fat Service

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Service exceeds recommended complexity.

Typical indicators:

* > 500 lines
* multiple workflows

Impact:

Low cohesion.

Recommendation:

Split by use case.

---

## AP203 - Duplicate Code

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Repeated logic across files or modules.

Impact:

Maintenance cost.

Recommendation:

Extract reusable abstractions.

---

## AP204 - Dead Code

Severity:

```text
LOW
```

(See severity-matrix.md)

Detection:

Unused:

* functions
* classes
* imports
* modules

Impact:

Noise.

Recommendation:

Remove dead code.

---

## AP205 - Excessive Nesting

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Nested conditions exceeding three levels.

Example:

```python
if a:
    if b:
        if c:
            if d:
```

Impact:

Reduced readability.

Recommendation:

Use guard clauses.

---

## AP206 - Long Function

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Function exceeds recommended length.

Typical indicator:

```text
>100 lines
```

Impact:

Difficult comprehension.

Recommendation:

Extract methods.

---

# CONFIGURATION

## AP300 - Hardcoded Configuration

Severity:

```text
HIGH
```

(See severity-matrix.md)

Detection:

Environment-specific values embedded in source code.

Examples:

* database URLs
* API URLs
* credentials
* runtime configuration

Impact:

Deployment risk.

Recommendation:

Use configuration layer.

---

## AP301 - Missing Environment Variables

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Configuration values expected but not externalized.

Impact:

Deployment fragility.

Recommendation:

Centralize configuration.

---

# DATABASE

## AP400 - N+1 Query Pattern

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Repeated database calls inside loops.

Example:

```python
for user in users:
    get_orders(user.id)
```

Impact:

Performance degradation.

Recommendation:

Use eager loading or batching.

---

## AP401 - Missing Database Abstraction

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Persistence logic scattered throughout application.

Impact:

Maintenance cost.

Recommendation:

Centralize persistence responsibilities.

---

# API DESIGN

## AP600 - Inconsistent Route Naming

Severity:

```text
LOW
```

(See severity-matrix.md)

Detection:

Mixed route naming conventions.

Examples:

```text
/users
GetOrders
create-product
```

Impact:

Poor API consistency.

Recommendation:

Standardize naming conventions.

---

## AP601 - Missing Error Handling

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Detection:

Unhandled exceptions or missing error boundaries.

Impact:

Unstable runtime behavior.

Recommendation:

Implement centralized exception handling.

---

# CODE QUALITY

## AP700 - Magic Numbers

Severity:

```text
LOW
```

(See severity-matrix.md)

Detection:

Unexplained numeric literals.

Example:

```python
if score > 87:
```

Impact:

Reduced readability.

Recommendation:

Use named constants.

---

## AP701 - Poor Naming

Severity:

```text
LOW
```

(See severity-matrix.md)

Detection:

Non-descriptive identifiers.

Examples:

```python
a
b
x
temp
```

Impact:

Reduced maintainability.

Recommendation:

Use meaningful names.

---

## AP702 - Excessive Comments

Severity:

```text
LOW
```

(See severity-matrix.md)

Detection:

Comments explaining obvious code.

Impact:

Noise.

Recommendation:

Improve code readability instead of commenting obvious behavior.

---

# Reporting Rules

Every finding must include:

* ID
* Severity
* File
* Line Range
* Evidence
* Impact
* Recommendation

---

# Example Finding

```text
ID: AP101

Severity: HIGH

File:
controllers/order_controller.py

Lines:
42-68

Evidence:
Discount calculation and pricing rules implemented inside controller.

Impact:
Violates MVC separation of concerns.

Recommendation:
Move business rules to OrderService.
```

---

# Evidence Rules

Every finding must contain objective evidence.

Bad:

```text
Controller looks too large.
```

Good:

```text
Controller contains 312 lines and performs request handling,
business logic and database access.
```

No evidence means no finding.

---

# Validation Rules

Do not report findings based solely on:

* project structure
* naming conventions
* assumptions

Use implementation evidence.

Evidence is mandatory.

---

# Final Rule

Anti-pattern detection must be implementation-driven.

Folder names do not prove architectural violations.

Evidence is required for every finding.

No evidence means no finding.