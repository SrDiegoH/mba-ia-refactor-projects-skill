# Transformation Priority

## Purpose

Define the priority order for architectural transformations during migration.

This document answers:

```text
What should be fixed first?
```

The objective is to ensure migrations:

* minimize risk
* maximize architectural impact
* preserve behavior
* remain incremental

Priority must be based on:

* severity
* architectural impact
* migration risk

Not developer preference.

---

# Core Principle

Always prioritize:

```text
Safety
↓
Architecture
↓
Maintainability
↓
Modernization
```

Never invert this order.

Example:

Correct:

```text
Fix architecture
Validate behavior
Upgrade dependencies
```

Incorrect:

```text
Upgrade dependencies
Refactor architecture
Debug everything
```

---

# Transformation Categories

## Category 1

```text
CRITICAL REMEDIATION
```

Highest priority.

Must be addressed immediately.

Examples:

* security vulnerabilities
* hardcoded credentials
* SQL injection
* command injection
* critical dependency risks

Reference:

```text
severity-matrix.md
```

---

## Category 2

```text
ARCHITECTURAL VIOLATIONS
```

Second highest priority.

Examples:

* business logic in routes
* business logic in controllers
* direct database access in controllers
* layer bypass
* circular dependencies

Reference:

```text
anti-pattern-catalog.md
```

---

## Category 3

```text
STRUCTURAL IMPROVEMENTS
```

Examples:

* missing service layer
* poor module organization
* dependency direction problems
* cohesion improvements

Goal:

Establish target architecture.

---

## Category 4

```text
MAINTAINABILITY IMPROVEMENTS
```

Examples:

* duplicate code
* long methods
* fat services
* dead code

Goal:

Improve maintainability.

---

## Category 5

```text
MODERNIZATION
```

Examples:

* deprecated APIs
* legacy framework patterns
* dependency upgrades

Goal:

Reduce future migration cost.

Modernization must never happen before architecture stabilization.

---

# Priority Matrix

## Priority 1

Address:

```text
CRITICAL
```

findings.

Examples:

```text
AP001
AP002
AP003
AP004
DH005
```

Required Action:

Immediate remediation.

---

## Priority 2

Address:

```text
HIGH
```

findings.

Examples:

```text
AP100
AP101
AP102
AP103
AP104
AP105
AP106
DH003
DH006
```

Goal:

Achieve architectural correctness.

---

## Priority 3

Address:

```text
MEDIUM
```

findings.

Examples:

```text
AP201
AP202
AP203
AP205
AP206
DA001
DA002
DA003
DH008
```

Goal:

Improve maintainability.

---

## Priority 4

Address:

```text
LOW
```

findings.

Examples:

```text
AP204
AP600
AP700
AP701
AP702
DA005
DA006
```

Goal:

Optional quality improvements.

---

## Priority 5

Review:

```text
INFO
```

findings.

No remediation required.

---

# MVC Transformation Order

When migrating to MVC:

Apply transformations in the following order.

---

## Step 1

Remove business logic from routes.

Before:

```text
Route
  ├─ Validation
  ├─ Database
  ├─ Business Rules
  └─ Response
```

After:

```text
Route
  └─ Controller
```

Applicable Findings:

```text
AP100
```

---

## Step 2

Remove business logic from controllers.

Before:

```text
Controller
  ├─ Business Rules
  ├─ Calculations
  └─ Workflows
```

After:

```text
Controller
  └─ Service
```

Applicable Findings:

```text
AP101
```

---

## Step 3

Remove persistence access from controllers.

Before:

```text
Controller
  └─ ORM
```

After:

```text
Controller
  └─ Service
        └─ ORM
```

Applicable Findings:

```text
AP102
AP103
```

---

## Step 4

Introduce missing service layer.

Before:

```text
Controller
  ↓
Model
```

After:

```text
Controller
  ↓
Service
  ↓
Model
```

Applicable Findings:

```text
AP104
```

---

## Step 5

Fix dependency direction.

Target:

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Model
```

Applicable Findings:

```text
AP105
```

---

## Step 6

Break circular dependencies.

Applicable Findings:

```text
AP106
```

---

# Refactoring Sequence

Preferred sequence:

```text
1. Audit
2. Plan
3. Fix Critical Findings
4. Fix High Findings
5. Stabilize Architecture
6. Validate Behavior
7. Fix Medium Findings
8. Validate Behavior
9. Modernize APIs
10. Upgrade Dependencies
11. Final Validation
```

---

# Dependency Transformation Rules

Never prioritize:

```text
Dependency Upgrade
```

before:

```text
Architecture Stabilization
```

Incorrect:

```text
Flask 1.x → Flask 3.x
while
controllers still contain business logic
```

Correct:

```text
Stabilize MVC
Validate
Upgrade Flask
Validate
```

---

# Deprecated API Rules

Deprecated APIs are important.

However:

```text
Deprecated API
```

is usually lower priority than:

```text
Business Logic In Controller
```

Reason:

Architecture issues create larger long-term maintenance costs.

Priority order:

```text
Architecture
↓
Maintainability
↓
Modernization
```

---

# Large Project Strategy

For large projects:

Prefer:

```text
Module-by-Module Migration
```

Instead of:

```text
Full System Migration
```

Example:

```text
Users Module
  ↓
Orders Module
  ↓
Products Module
```

Benefits:

* lower risk
* easier validation
* easier rollback

---

# Validation Gates

Before moving to the next priority level:

Validation is required.

Example:

```text
Fix High Findings
↓
Validate
↓
Fix Medium Findings
```

Never stack multiple transformation categories without validation.

---

# Escalation Rules

If a transformation would:

* change business behavior
* change endpoint contracts
* change database schema
* change authentication behavior

then stop.

Status:

```text
REQUIRES_HUMAN_REVIEW
```

Reference:

```text
safety-rules.md
```

---

# Completion Criteria

Architecture migration is considered complete when:

* no CRITICAL findings remain
* no HIGH findings remain
* target dependency flow is achieved
* validation passes
* behavioral parity is confirmed

Only then should modernization begin.

---

# Final Rule

When choosing between two transformations:

Prefer the transformation that:

1. reduces architectural risk
2. preserves behavior
3. improves separation of concerns
4. minimizes migration complexity

Never prioritize modernization over architectural correctness.