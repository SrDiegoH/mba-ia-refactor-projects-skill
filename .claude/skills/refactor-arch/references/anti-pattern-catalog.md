# Anti Pattern Catalog

## AP001 — Hardcoded Credentials

Severity: CRITICAL

Detection:

SECRET_KEY=
PASSWORD=
TOKEN=

Examples:

app.config["SECRET_KEY"]="abc"

---

## AP002 — SQL Injection

Severity: CRITICAL

Detection:

SQL query concatenation.

Examples:

"SELECT * FROM users WHERE id="+id

---

## AP003 — Arbitrary SQL Execution

Severity: CRITICAL

Detection:

execute(user_input)

Examples:

cursor.execute(sql)

---

## AP004 — God Class

Severity: HIGH

Detection:

Class/file > 300 lines

AND

Contains:

- DB access
- business logic
- routing

---

## AP005 — Plaintext Passwords

Severity: HIGH

Detection:

password field stored directly.

Examples:

INSERT senha

WHERE senha=?

---

## AP006 — Business Logic In Controllers

Severity: HIGH

Detection:

Loops
Calculations
Pricing
Validation

inside routes/controllers.

---

## AP007 — Global Mutable State

Severity: HIGH

Detection:

Global database connection
Global caches

---

## AP008 — Deprecated APIs

Severity: MEDIUM

Detection:

Framework deprecated methods.

Must verify framework version.

---

## AP009 — N+1 Queries

Severity: MEDIUM

Detection:

Query inside loop.

---

## AP010 — Missing Validation

Severity: MEDIUM

Detection:

Request body used directly.

---

## AP011 — Magic Strings

Severity: LOW

Detection:

Repeated literals.

---

## AP012 — Print Debugging

Severity: LOW

Detection:

print()
console.log()

---

## AP013 — Code Duplication

Severity: LOW

Detection:

Repeated blocks > 5 lines