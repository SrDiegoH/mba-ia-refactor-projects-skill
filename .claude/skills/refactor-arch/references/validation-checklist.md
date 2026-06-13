# Validation Checklist

This checklist must be executed after every refactoring.

The refactoring is considered successful only if ALL validation steps pass.

---

# Phase 3 Validation

## 1. Structural Validation

Verify that the project follows MVC principles.

Required:

- Models layer exists
- Controllers layer exists
- Routes/Views layer exists
- Configuration layer exists
- Entry point exists
- Error handling is centralized

Checklist

[ ] Models created

[ ] Controllers created

[ ] Routes created

[ ] Configuration extracted

[ ] Error handling centralized

[ ] Clear application entry point

---

## 2. Anti-Pattern Validation

Verify that previously detected findings were addressed.

Checklist

[ ] No hardcoded credentials

[ ] No SQL injection

[ ] No arbitrary SQL execution

[ ] No God Class remaining

[ ] No business logic in routes

[ ] No global mutable state

[ ] No plaintext passwords

[ ] No deprecated APIs

---

## 3. Application Boot Validation

Verify application starts correctly.

Python

Examples:

```bash
python app.py
```

or

```bash
flask run
```

Node

```bash
npm start
```

or

```bash
node src/app.js
```

Checklist

[ ] Application starts successfully

[ ] No startup exceptions

[ ] Dependencies resolved

[ ] Database connection successful

---

## 4. Endpoint Smoke Test

Collect all existing routes before refactoring.

After refactoring verify they still exist.

Examples

GET /products

POST /products

GET /orders

POST /orders

Checklist

[ ] All original endpoints preserved

[ ] Success responses returned

[ ] Error responses handled correctly

[ ] Authentication flows still work

---

## 5. Data Integrity Validation

Verify no data corruption.

Checklist

[ ] Existing records readable

[ ] Create operations working

[ ] Update operations working

[ ] Delete operations working

[ ] Relationships preserved

---

## 6. Security Validation

Checklist

[ ] Secrets moved to environment variables

[ ] SQL parameterization applied

[ ] User input validated

[ ] Sensitive data not exposed

[ ] Admin operations protected

---

## 7. Architecture Validation

Models

[ ] No HTTP logic

[ ] No route declarations

Controllers

[ ] No SQL statements

[ ] No direct persistence

Routes

[ ] No business rules

[ ] No database access

Configuration

[ ] Externalized

[ ] Environment-driven

---

# Validation Report Template

================================
VALIDATION REPORT
================================

Project:

Boot Validation:
PASS / FAIL

Endpoint Validation:
PASS / FAIL

Data Integrity:
PASS / FAIL

Security Validation:
PASS / FAIL

Architecture Validation:
PASS / FAIL

Overall Result:

PASS
or
FAIL

================================

The skill MUST NOT claim success if any item fails.