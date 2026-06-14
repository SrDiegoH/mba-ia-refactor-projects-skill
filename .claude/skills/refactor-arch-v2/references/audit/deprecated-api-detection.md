# Deprecated API Detection

## Purpose

Detect deprecated APIs, methods, imports, decorators, configuration patterns and framework features that should be modernized during refactoring.

The objective is not to upgrade every dependency.

The objective is to identify code that introduces:

* maintenance risks
* upgrade blockers
* compatibility risks
* future migration costs

Detection must be evidence-based.

Never report a deprecated API without evidence.

---

# Severity Assignment

Severity classification is defined in:

```text
severity-matrix.md
```

This document only assigns severity levels.

Severity definitions must not be duplicated here.

---

# Scope Boundary

This document covers:

* deprecated APIs
* deprecated methods
* deprecated imports
* deprecated decorators
* deprecated framework features
* deprecated configuration patterns
* removed APIs still in use

This document does NOT cover:

* abandoned dependencies
* archived projects
* dependency maintenance status
* dependency security posture
* dependency lifecycle analysis

Those concerns are handled by:

```text
dependency-health-rules.md
```

---

# Detection Process

## Step 1 - Dependency Inspection

Inspect:

* requirements.txt
* pyproject.toml
* package.json
* package-lock.json
* yarn.lock
* pnpm-lock.yaml

Identify libraries that may introduce deprecated APIs.

Do not report findings yet.

Use dependencies only as supporting evidence.

---

## Step 2 - Import Analysis

Inspect all imports.

Examples:

Python:

```python
import imp
```

```python
import distutils
```

```python
import pkg_resources
```

Node.js:

```javascript
require("uuid/v4")
```

Deprecated imports are strong indicators.

---

## Step 3 - API Usage Analysis

Inspect:

* method calls
* decorators
* initialization patterns
* framework APIs
* ORM APIs

Examples:

```python
asyncio.get_event_loop()
```

```python
session.query(...)
```

---

## Step 4 - Configuration Analysis

Inspect:

* framework initialization
* configuration files
* startup code

Look for deprecated configuration mechanisms.

---

## Step 5 - Warning Detection

Inspect source code and runtime artifacts.

Examples:

```python
DeprecationWarning
```

```python
PendingDeprecationWarning
```

These are considered strong evidence.

---

## Step 6 - Documentation Evidence

When available, verify findings using:

* official documentation
* official migration guides
* framework release notes
* language documentation
* official deprecation notices

Prefer official sources.

---

# Detection Categories

## DA001 - Deprecated Standard Library API

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Definition:

A language standard library feature officially deprecated.

Impact:

Future compatibility issues.

Recommendation:

Replace with supported alternatives.

---

## DA002 - Deprecated Framework API

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Definition:

Framework API officially marked as deprecated.

Impact:

Upgrade blockers.

Recommendation:

Migrate to supported framework APIs.

---

## DA003 - Deprecated ORM API

Severity:

```text
MEDIUM
```

(See severity-matrix.md)

Definition:

ORM feature marked as legacy or deprecated.

Impact:

Future migration complexity.

Recommendation:

Adopt current ORM patterns.

---

## DA004 - Removed API Usage

Severity:

```text
HIGH
```

(See severity-matrix.md)

Definition:

Code references APIs already removed from supported versions.

Impact:

Application may fail after framework or language upgrades.

Recommendation:

Immediate migration required.

---

## DA005 - Legacy Framework Pattern

Severity:

```text
LOW
```

(See severity-matrix.md)

Definition:

Pattern superseded by newer framework approaches.

Pattern is still functional but no longer recommended.

Impact:

Reduced maintainability.

Recommendation:

Modernize when appropriate.

---

## DA006 - Deprecated Configuration Pattern

Severity:

```text
LOW
```

(See severity-matrix.md)

Definition:

Configuration mechanism officially deprecated.

Impact:

Upgrade friction.

Recommendation:

Migrate to supported configuration models.

---

# Python Detection Rules

## imp Module

Detection:

```python
import imp
```

Classification:

```text
DA001
```

Recommendation:

```python
import importlib
```

---

## distutils

Detection:

```python
import distutils
```

Classification:

```text
DA001
```

Recommendation:

Use:

```text
setuptools
packaging
```

depending on use case.

---

## pkg_resources

Detection:

```python
import pkg_resources
```

Classification:

```text
DA001
```

Recommendation:

```python
importlib.metadata
```

---

## asyncio.get_event_loop()

Detection:

```python
asyncio.get_event_loop()
```

Classification:

```text
DA002
```

Recommendation:

```python
asyncio.get_running_loop()
```

---

## asyncore

Detection:

```python
import asyncore
```

Classification:

```text
DA001
```

---

## asynchat

Detection:

```python
import asynchat
```

Classification:

```text
DA001
```

---

# Flask Detection Rules

Only report deprecated Flask APIs when official deprecation evidence exists.

Evidence is mandatory.

---

# FastAPI Detection Rules

Only report deprecated FastAPI APIs when official documentation confirms deprecation.

Evidence is mandatory.

---

# Django Detection Rules

Detect settings or APIs officially marked as deprecated.

Classification:

```text
DA002
```

or

```text
DA006
```

depending on context.

---

# SQLAlchemy Detection Rules

## Legacy Query API

Detection:

```python
session.query(...)
```

Classification:

```text
DA003
```

Severity:

```text
LOW
```

(See severity-matrix.md)

Confidence:

```text
MEDIUM
```

Recommendation:

```python
select(...)
```

---

# Node.js Detection Rules

## uuid/v4 Import

Detection:

```javascript
require("uuid/v4")
```

Classification:

```text
DA002
```

Recommendation:

```javascript
const { v4: uuidv4 } = require("uuid")
```

---

## sys Module

Detection:

```javascript
require("sys")
```

Classification:

```text
DA001
```

Recommendation:

```javascript
require("util")
```

---

# Evidence Requirements

Deprecation findings must be supported by at least one of:

* official documentation
* framework release notes
* migration guide
* deprecation warning
* language specification
* official deprecation notice

Community opinions are not sufficient evidence.

---

# Confidence Levels

## HIGH

Direct official evidence exists.

## MEDIUM

Strong indirect evidence exists.

## LOW

Possible deprecation detected but official confirmation unavailable.

---

# Reporting Format

Every finding must include:

* ID
* Severity
* Confidence
* File
* Line Range
* Deprecated Element
* Evidence
* Recommended Replacement
* Migration Complexity

---

# Validation Rules

Do not report deprecated APIs solely because they are old.

Old does not mean deprecated.

Do not report preferred modern alternatives unless an official deprecation exists.

Evidence is mandatory.

No evidence means no finding.

---

# Final Rule

Only report deprecations supported by evidence.

Prefer missing a deprecation over reporting a false positive.