# Post-Refactor Checklist

## Purpose

Provide a final verification checklist that must be completed after architectural refactoring and before declaring the migration successful.

This checklist consolidates all validation phases and serves as the final migration gate.

A migration is not considered complete until every applicable checklist item has been reviewed.

---

# Usage Rules

This checklist must be executed after:

```text
Boot Validation
Architecture Validation
Endpoint Validation
Behavioral Validation
```

and before:

```text
Migration Completion
```

---

# Checklist Principles

## Evidence Required

Every checklist item must be supported by evidence.

Invalid:

```text
Looks correct.
```

Valid:

```text
All controllers delegate to services.
Verified through dependency analysis.
```

---

## Unknown Is Not Pass

If verification cannot be completed:

Status:

```text
UNKNOWN
```

Do not mark:

```text
PASS
```

without evidence.

---

## Human Review Overrides

If any item requires human validation:

Status:

```text
REQUIRES_HUMAN_REVIEW
```

Migration cannot be approved automatically.

---

# Section 1 - Startup Validation

Reference:

```text
boot-validation.md
```

---

## PC001

Verify:

Application starts successfully.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC002

Verify:

Startup entry point exists.

Examples:

```text
app.py
main.py
server.js
index.js
```

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC003

Verify:

Imports resolve successfully.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC004

Verify:

No circular imports exist.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC005

Verify:

Framework initializes successfully.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC006

Verify:

Configuration loads successfully.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC007

Verify:

Routes register successfully.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC008

Verify:

Models load successfully.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Section 2 - Architecture Validation

Reference:

```text
architecture-validation.md
```

---

## PC009

Verify:

Target architecture achieved.

Expected:

```text
MVC
```

or

```text
MVC_WITH_SERVICES
```

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC010

Verify:

Dependency flow is compliant.

Expected:

```text
Route
 ↓
Controller
 ↓
Service
 ↓
Model
```

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC011

Verify:

No forbidden dependencies remain.

Examples:

```text
Route → Model
Controller → Database
Model → Controller
```

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC012

Verify:

No circular dependencies remain.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC013

Verify:

Layer responsibilities are respected.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Section 3 - Audit Findings Validation

Reference:

```text
anti-pattern-catalog.md
```

---

## PC014

Verify:

All CRITICAL findings resolved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC015

Verify:

All HIGH findings resolved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC016

Verify:

No new CRITICAL findings introduced.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC017

Verify:

No new HIGH findings introduced.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC018

Verify:

No architectural regressions introduced.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Section 4 - Endpoint Validation

Reference:

```text
endpoint-validation.md
```

---

## PC019

Verify:

All inventoried endpoints still exist.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC020

Verify:

HTTP methods preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC021

Verify:

Endpoint paths preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC022

Verify:

Request contracts preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC023

Verify:

Response contracts preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC024

Verify:

Status codes preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC025

Verify:

Authentication requirements preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC026

Verify:

Authorization requirements preserved.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Section 5 - Behavioral Validation

Reference:

```text
behavioral-validation.md
```

---

## PC027

Verify:

Business rules unchanged.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC028

Verify:

Application workflows unchanged.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC029

Verify:

Persistence behavior unchanged.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC030

Verify:

Error handling behavior unchanged.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC031

Verify:

External integrations unchanged.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Section 6 - Safety Validation

Reference:

```text
safety-rules.md
```

---

## PC032

Verify:

No business rules changed.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC033

Verify:

No endpoint contracts changed.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC034

Verify:

No database schema changed.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC035

Verify:

No authentication behavior changed.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC036

Verify:

No authorization behavior changed.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC037

Verify:

No external integrations changed.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC038

Verify:

No dependency upgrades performed unintentionally.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Section 7 - Modernization Validation

Applicable only when modernization is requested.

Reference:

```text
deprecated-api-detection.md
```

---

## PC039

Verify:

Deprecated APIs removed correctly.

Status:

```text
PASS
FAIL
UNKNOWN
N/A
```

---

## PC040

Verify:

Replacement APIs are compatible.

Status:

```text
PASS
FAIL
UNKNOWN
N/A
```

---

## PC041

Verify:

Modernization introduced no regressions.

Status:

```text
PASS
FAIL
UNKNOWN
N/A
```

---

# Section 8 - Documentation Validation

## PC042

Verify:

Architecture report updated.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC043

Verify:

Audit report updated.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC044

Verify:

Migration plan reflects completed work.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

## PC045

Verify:

Validation reports generated.

Status:

```text
PASS
FAIL
UNKNOWN
```

---

# Migration Approval Rules

## APPROVED

Conditions:

```text
All mandatory checks PASS
No FAIL items
No regressions
```

---

## APPROVED_WITH_REVIEW

Conditions:

```text
No FAIL items
One or more UNKNOWN items
Human validation required
```

---

## REJECTED

Conditions:

```text
One or more FAIL items
```

Migration must not be approved.

---

# Final Report Template

```text
Post-Refactor Checklist

Startup Validation:
PASS

Architecture Validation:
PASS

Endpoint Validation:
PASS

Behavioral Validation:
PASS

Safety Validation:
PASS

Modernization Validation:
N/A

Documentation Validation:
PASS

Overall Status:
APPROVED
```

---

# Escalation Rules

Immediately escalate if any of the following occur:

* application no longer starts
* endpoint removed
* request contract changed
* response contract changed
* database schema changed
* authentication behavior changed
* authorization behavior changed
* business rules changed

Status:

```text
REQUIRES_HUMAN_REVIEW
```

---

# Completion Criteria

A migration is considered complete only when:

* startup validation passes
* architecture validation passes
* endpoint validation passes
* behavioral validation passes
* safety validation passes
* no regressions exist

---

# Final Rule

Architectural improvements are not the success criterion.

Migration success is achieved only when:

```text
Architecture Improved
+
Behavior Preserved
+
Validation Passed
```

All three conditions are mandatory.