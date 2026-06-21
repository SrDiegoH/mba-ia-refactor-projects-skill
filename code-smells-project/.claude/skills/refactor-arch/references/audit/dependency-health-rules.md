# Dependency Health Rules

## Purpose

Evaluate dependency health, support status, maintenance activity and security posture.

This analysis is separate from deprecated API detection.

A dependency may be healthy while exposing deprecated APIs.

A dependency may also be unhealthy even when no deprecated APIs are used.

Dependency health findings help identify future maintenance, security and upgrade risks.

---

# Severity Assignment

Severity classification is defined in:

severity-matrix.md

This document only assigns severity levels.

Severity criteria must not be redefined here.

---

# Scope

This document covers:

- dependency maintenance status
- dependency support status
- dependency lifecycle status
- archived projects
- abandoned projects
- end-of-life software
- known security risks
- unsupported framework versions

This document does NOT cover:

- deprecated methods
- deprecated imports
- deprecated framework APIs
- deprecated ORM APIs

Those concerns belong to:

```text
deprecated-api-detection.md
```

---

# Detection Process

Execute all steps.

---

# Step 1 - Dependency Discovery

Inspect:

- requirements.txt
- pyproject.toml
- poetry.lock
- Pipfile
- package.json
- package-lock.json
- yarn.lock
- pnpm-lock.yaml
- composer.json

Identify all direct dependencies.

When lock files exist, use them to determine actual installed versions.

---

# Step 2 - Framework Identification

Identify:

- application framework
- ORM
- authentication libraries
- database drivers
- infrastructure libraries

Framework dependencies require higher scrutiny because they affect large portions of the project.

---

# Step 3 - Support Status Analysis

Determine whether each dependency is:

- actively maintained
- deprecated
- archived
- end-of-life
- unsupported

Evidence should come from:

- official documentation
- package registry notices
- repository status
- maintainer announcements

---

# Step 4 - Security Analysis

Identify:

- known vulnerabilities
- critical vulnerabilities
- unsupported vulnerable versions

Use official security advisories whenever possible.

---

# Step 5 - Upgrade Risk Analysis

Determine whether a dependency creates:

- framework upgrade blockers
- runtime upgrade blockers
- language version upgrade blockers

Examples:

- Python 3.12 incompatibilities
- Node.js version incompatibilities
- ORM version lock-in

---

# Health Categories

---

# DH001 - Deprecated Dependency

Severity:

MEDIUM

(See severity-matrix.md)

Definition:

Dependency officially marked as deprecated.

Evidence Required:

- package registry warning
- official maintainer announcement
- official documentation

Impact:

Future maintenance risk.

Recommendation:

Replace with supported alternative.

---

# DH002 - Archived Dependency

Severity:

MEDIUM

(See severity-matrix.md)

Definition:

Repository archived.

Project is read-only.

No future development expected.

Evidence Required:

- repository archived flag
- official maintainer statement

Impact:

No future fixes or improvements.

Recommendation:

Plan migration.

---

# DH003 - End Of Life Dependency

Severity:

HIGH

(See severity-matrix.md)

Definition:

Dependency has reached end-of-life.

No support is available.

Evidence Required:

- vendor announcement
- support lifecycle documentation

Impact:

Security and maintenance risk.

Recommendation:

Upgrade immediately.

---

# DH004 - Unmaintained Dependency

Severity:

LOW

(See severity-matrix.md)

Definition:

Project shows no meaningful maintenance activity.

Examples:

- no releases for years
- no commits for years
- no maintainer activity

Evidence Required:

Maintenance indicators.

Impact:

Increasing future risk.

Recommendation:

Monitor or replace.

---

# DH005 - Known Security Risk

Severity:

CRITICAL

(See severity-matrix.md)

Definition:

Dependency contains known security vulnerabilities.

Evidence Required:

- CVE
- security advisory
- official vulnerability disclosure

Impact:

Potential security compromise.

Recommendation:

Immediate remediation.

---

# DH006 - Unsupported Framework Version

Severity:

HIGH

(See severity-matrix.md)

Definition:

Project uses framework version no longer supported.

Examples:

- unsupported Flask version
- unsupported Django version
- unsupported Express version

Impact:

Security and upgrade risks.

Recommendation:

Upgrade framework.

---

# DH007 - Unsupported Runtime Dependency

Severity:

HIGH

(See severity-matrix.md)

Definition:

Dependency incompatible with supported runtime versions.

Examples:

- Python version incompatibility
- Node.js version incompatibility

Impact:

Upgrade blocker.

Recommendation:

Replace or upgrade dependency.

---

# DH008 - Upgrade Blocker Dependency

Severity:

MEDIUM

(See severity-matrix.md)

Definition:

Dependency prevents framework or runtime upgrades.

Impact:

Long-term technical debt.

Recommendation:

Evaluate migration path.

---

# Confidence Levels

## HIGH

Official evidence exists.

Examples:

- archived repository
- EOL announcement
- CVE publication
- deprecation notice

---

## MEDIUM

Strong indirect evidence exists.

Examples:

- no releases
- abandoned maintenance
- unsupported version matrix

---

## LOW

Evidence is incomplete.

Additional validation recommended.

---

# Reporting Format

Every finding must include:

- ID
- Severity
- Confidence
- Dependency
- Current Version
- Evidence
- Impact
- Recommendation
- Migration Complexity

---

# Example Output

ID: DH003

Severity: HIGH

Confidence: HIGH

Dependency:
Flask

Current Version:
1.0

Evidence:
Framework version is no longer supported.

Impact:
No security updates available.

Recommendation:
Upgrade to a supported version.

Migration Complexity:
MEDIUM

---

# Migration Complexity

Possible values:

LOW

Examples:

- patch version upgrade
- minor version upgrade

---

MEDIUM

Examples:

- major version upgrade
- configuration updates
- API adjustments

---

HIGH

Examples:

- framework migration
- ORM replacement
- large-scale dependency replacement

---

# Validation Rules

Do not report a dependency solely because it is old.

Old does not mean unhealthy.

Do not report a dependency solely because a newer version exists.

Newer does not imply risk.

Evidence is required.

No evidence means no finding.

---

# Refactoring Rules

Dependency upgrades must preserve behavior.

Prefer minimal-risk upgrades.

When possible:

1. Complete architectural refactoring.
2. Validate behavior.
3. Upgrade dependencies.
4. Validate behavior again.

Do not combine major dependency upgrades and major architectural migrations in the same change set.

---

# Final Rule

Only report dependency health findings supported by evidence.

Prefer a false negative over a false positive.

Every finding must be traceable to objective evidence.