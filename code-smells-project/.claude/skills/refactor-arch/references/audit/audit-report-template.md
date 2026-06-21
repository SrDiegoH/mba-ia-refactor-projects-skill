# Audit Report Template Specification

## Purpose

Define the mandatory structure for all architecture audit reports generated during Phase 2.

All reports must follow this template.

Sections may not be omitted.

Fields may only be marked as:

* NOT FOUND
* NOT APPLICABLE
* UNKNOWN

when evidence is insufficient.

---

# Report Generation Process

Generate the report after:

1. Stack detection
2. Architecture detection
3. Domain detection
4. Endpoint inventory
5. Anti-pattern analysis
6. Deprecated API analysis

The report must be completed before any refactoring occurs.

After generating the report:

STOP.

Request user confirmation.

Example:

```text
Proceed with refactoring (Phase 3)? [y/n]
```

Never continue automatically.

---

# Required Report Structure

The report must contain the following sections in order.

---

## PROJECT INFORMATION

Required Fields:

* Project Name
* Analysis Date
* Language
* Framework
* Database
* ORM
* Package Manager
* Architecture
* Domain
* Confidence
* Files Analyzed
* Estimated LOC

---

## PHASE 1 SUMMARY

Required Fields:

* Stack Detection Status
* Architecture Detection Status
* Domain Detection Status
* Endpoint Inventory Status

---

## ENDPOINT INVENTORY SUMMARY

Required Fields:

* Total Endpoints
* GET Count
* POST Count
* PUT Count
* PATCH Count
* DELETE Count
* Protected Endpoints
* Public Endpoints

---

## AUDIT SUMMARY

Required Fields:

* Critical Findings
* High Findings
* Medium Findings
* Low Findings
* Total Findings

---

## CRITICAL FINDINGS

Include every finding with:

* ID
* Severity
* File
* Line Range
* Evidence
* Impact
* Recommendation

---

## HIGH FINDINGS

Same structure.

---

## MEDIUM FINDINGS

Same structure.

---

## LOW FINDINGS

Same structure.

---

## DEPRECATED APIS

Required Fields:

* API
* File
* Lines
* Reason
* Recommended Replacement
* Migration Complexity

---

## MVC MIGRATION PLAN

Required Fields:

* Selected Migration Strategy
* Reason
* Planned Changes
* Expected Target Architecture

---

## RISK ASSESSMENT

Required Fields:

* Low Risk Changes
* Medium Risk Changes
* High Risk Changes
* Potential Breaking Changes

---

## REFACTORING CHECKLIST

Required Fields:

* Security
* Architecture
* Configuration
* Controllers
* Services
* Models
* Routes
* Validation

All items should start unchecked.

---

## VALIDATION PLAN

Required Fields:

* Boot Validation
* Endpoint Validation
* Architecture Validation
* Configuration Validation

Status should initially be:

```text
NOT VERIFIED
```

---

## FINAL STATUS

Required Fields:

* Findings Open
* Findings Resolved
* Migration Readiness

Possible Values:

```text
READY
NOT_READY
REQUIRES_REVIEW
```

---

# Finding Format

Every finding must use the following structure.

```text
ID: AP101

Severity: HIGH

Title:
Business Logic In Controller

File:
controllers/order_controller.py

Lines:
42-68

Evidence:
Discount calculation found inside controller.

Impact:
Violates MVC separation of concerns.

Recommendation:
Move calculation to OrderService.

Status:
OPEN
```

---

# Evidence Rules

Every finding must contain evidence.

Bad:

```text
Controller looks too large.
```

Good:

```text
Controller contains 312 lines and implements
request handling, persistence and business rules.
```

No evidence means no finding.

---

# Severity Ordering

Always order findings:

1. CRITICAL
2. HIGH
3. MEDIUM
4. LOW

Never mix severities.

---

# Line Number Rules

Always report line numbers when available.

Example:

```text
Lines: 42-68
```

If unavailable:

```text
Lines: UNKNOWN
```

Never invent line numbers.

---

# Report Quality Requirements

Minimum report quality:

* At least one finding when issues exist.
* Exact file paths whenever possible.
* Exact evidence whenever possible.
* Concrete recommendations.

Avoid generic statements.

---

# Stop Condition

After generating the report:

1. Save report.
2. Present summary.
3. Ask for confirmation.

Do not refactor automatically.

Refactoring requires explicit user approval.

---

# Final Rule

The audit report is the authoritative artifact for Phase 3.

All refactoring decisions must be traceable to findings documented in the report.