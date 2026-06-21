# Severity Matrix

## Purpose

Define the severity classification system used throughout the audit process.

All findings must use the severity levels defined in this document.

This matrix applies to:

* anti-pattern findings
* deprecated API findings
* dependency health findings
* validation findings
* architecture findings

Severity determines:

* audit prioritization
* migration priority
* remediation order
* project readiness

---

# Severity Levels

The following levels are supported:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFO
```

Every finding must be assigned exactly one severity level.

---

# Classification Principles

Severity is determined by impact.

Do not classify based solely on technical complexity.

A simple issue may still be CRITICAL.

A complex issue may still be LOW.

Always evaluate:

* security impact
* operational impact
* architectural impact
* maintainability impact
* upgrade impact

---

# CRITICAL

## Definition

A finding that may cause:

* security compromise
* remote code execution
* data leakage
* data corruption
* authentication bypass
* production outage
* application failure

Immediate action required.

---

## Typical Examples

### Security

* hardcoded credentials
* SQL injection
* command injection
* authentication bypass
* exposed secrets

---

### Dependency Health

* actively exploited vulnerability
* critical CVE
* unsupported dependency with known security issue

---

### Validation

* application does not start
* endpoint completely broken
* production-breaking regression

---

## Examples

```text
AP001 - Hardcoded Credentials
```

```text
AP002 - SQL Injection Risk
```

```text
DH005 - Known Security Risk
```

---

## Migration Priority

```text
IMMEDIATE
```

---

# HIGH

## Definition

A finding that significantly affects:

* architecture
* maintainability
* reliability
* future development

Should be fixed before project completion.

---

## Typical Examples

### Architecture

* business logic in controller
* business logic in route
* layer bypass
* circular dependency

---

### Configuration

* hardcoded environment configuration
* missing configuration abstraction

---

### Validation

* endpoint contract change
* authentication behavior change

---

### Dependencies

* end-of-life dependency
* unsupported framework version

---

## Examples

```text
AP100 - Business Logic In Route
```

```text
AP101 - Business Logic In Controller
```

```text
AP106 - Circular Dependency
```

```text
DH003 - End Of Life Dependency
```

---

## Migration Priority

```text
HIGH
```

---

# MEDIUM

## Definition

A finding that increases technical debt but does not create immediate operational risk.

Should be fixed when practical.

---

## Typical Examples

### Maintainability

* duplicate code
* long methods
* excessive nesting
* fat service

---

### Deprecation

* deprecated API
* deprecated framework feature
* deprecated ORM API

---

### Database

* N+1 query patterns
* scattered persistence logic

---

## Examples

```text
AP202 - Fat Service
```

```text
AP203 - Duplicate Code
```

```text
AP205 - Excessive Nesting
```

```text
DA001 - Deprecated Standard Library API
```

```text
DA003 - Deprecated ORM API
```

---

## Migration Priority

```text
NORMAL
```

---

# LOW

## Definition

A finding that improves code quality or consistency but has limited operational impact.

Optional during migration.

---

## Typical Examples

### Code Quality

* magic numbers
* naming issues
* dead code
* legacy framework patterns

---

### Organization

* minor structure inconsistencies
* non-standard naming conventions

---

### Modernization

* obsolete but functional patterns
* optional refactoring opportunities

---

## Examples

```text
AP204 - Dead Code
```

```text
AP700 - Magic Numbers
```

```text
AP701 - Poor Naming
```

```text
DA005 - Legacy Framework Pattern
```

```text
DA006 - Deprecated Configuration Pattern
```

---

## Migration Priority

```text
OPTIONAL
```

---

# INFO

## Definition

Observation only.

No action required.

Included for visibility.

---

## Typical Examples

* architectural notes
* stack observations
* framework observations
* project metrics

---

## Examples

```text
Architecture: PARTIAL_MVC
```

```text
Framework: Flask
```

```text
Database: PostgreSQL
```

---

## Migration Priority

```text
NONE
```

---

# Severity Escalation Rules

Severity may be increased when multiple risk factors combine.

Example:

Normally:

```text
DA001
MEDIUM
```

But:

```text
DA001
+
Upgrade Blocker
+
Production Dependency
```

May become:

```text
HIGH
```

---

# Severity Downgrade Rules

Downgrading severity requires justification.

Example:

```text
Deprecated API
```

normally:

```text
MEDIUM
```

but:

```text
Unused code path
```

may justify:

```text
LOW
```

---

# Finding Requirements

Every finding must include:

* ID
* Severity
* Evidence
* Impact
* Recommendation

Severity without evidence is invalid.

---

# Audit Summary Calculation

Generate summary counts.

Example:

```text
Critical Findings: 1
High Findings: 4
Medium Findings: 7
Low Findings: 3
Info Findings: 5
```

---

# Readiness Rules

Migration readiness is determined by open findings.

---

## READY

Conditions:

```text
No CRITICAL findings
No HIGH findings
```

---

## REQUIRES_REVIEW

Conditions:

```text
High findings still open
```

---

## NOT_READY

Conditions:

```text
Critical findings present
```

---

# Refactoring Rules

During Phase 3:

Address findings in this order:

1. CRITICAL
2. HIGH
3. MEDIUM
4. LOW

INFO findings never require remediation.

---

# Final Rule

Severity reflects business and technical impact.

When uncertain:

Prefer the lower severity level and document the reasoning.