# Endpoint Inventory

## Purpose

Create a complete inventory of all public application endpoints before any modification is performed.

This inventory becomes the source of truth for endpoint validation after refactoring.

The inventory must be created during Phase 1.

The inventory must be reused during Phase 4.

Never perform refactoring before creating the inventory.

---

# Goals

The inventory serves four purposes:

1. Preserve API contracts.
2. Detect missing endpoints after refactoring.
3. Detect changed routes.
4. Validate endpoint behavior.

---

# Endpoint Discovery

Inspect all files that may register routes.

Examples:

Python:

* app.py
* routes.py
* blueprints
* routers
* views

Node.js:

* app.js
* server.js
* routes/
* routers/
* express.Router()

Framework-specific routing files should also be analyzed.

---

# Route Detection

Collect every public route.

Examples:

```python
@app.route("/users")
```

```python
@bp.route("/orders")
```

```python
router.get("/products")
```

```javascript
app.post("/checkout")
```

```javascript
router.delete("/users/:id")
```

---

# Required Fields

Every discovered endpoint must contain:

| Field                   | Required        |
| ----------------------- | --------------- |
| HTTP Method             | YES             |
| Route Path              | YES             |
| Handler                 | YES             |
| Source File             | YES             |
| Line Number             | YES             |
| Authentication Required | YES             |
| Request Body            | IF APPLICABLE   |
| Path Parameters         | IF APPLICABLE   |
| Query Parameters        | IF APPLICABLE   |
| Response Type           | IF IDENTIFIABLE |

---

# Endpoint Metadata

Capture as much information as possible.

Example:

```text
Method: GET

Route: /users/{id}

Handler: UserController.get_user

File: controllers/user_controller.py

Line: 52

Authentication: Required

Path Parameters:
- id

Query Parameters:
- include_orders

Response:
- User JSON
```

---

# Route Normalization

Normalize routes before storing.

Examples:

Convert:

```text
/users/<id>
```

to:

```text
/users/{id}
```

Convert:

```text
/users/:id
```

to:

```text
/users/{id}
```

Use a consistent format across frameworks.

---

# Authentication Detection

Attempt to identify endpoint protection.

Examples:

Python:

```python
@login_required
```

```python
@jwt_required()
```

Node:

```javascript
authMiddleware
```

```javascript
jwtMiddleware
```

Store:

```text
Authentication: Required
```

or

```text
Authentication: Not Required
```

---

# Request Schema Detection

When possible, identify:

Request Body Fields:

```json
{
  "name": "string",
  "email": "string"
}
```

Path Parameters:

```text
{id}
```

Query Parameters:

```text
?page=
?limit=
```

---

# Response Detection

When possible, identify:

Status Codes:

```text
200
201
204
400
401
404
500
```

Response Type:

```text
JSON
HTML
TEXT
FILE
STREAM
```

---

# Duplicate Routes

If duplicate routes are found:

Example:

```text
GET /users
```

defined multiple times.

Record all occurrences.

Flag for audit review.

Do not automatically discard duplicates.

---

# Versioned APIs

Preserve version information.

Examples:

```text
/api/v1/users
/api/v2/users
```

Treat each version as a separate endpoint.

---

# Dynamic Route Registration

If routes are dynamically generated:

Attempt to infer actual routes.

If impossible:

Record:

```text
Dynamic Route Detected

Validation Status:
PARTIAL
```

---

# Inventory Output Format

Always produce the inventory using the following structure.

```markdown
## Endpoint Inventory

| Method | Route | Handler | File | Line |
|----------|----------|----------|----------|----------|
| GET | /users | get_users | users.py | 45 |
| GET | /users/{id} | get_user | users.py | 68 |
| POST | /users | create_user | users.py | 92 |
```

---

# Inventory Summary

Always provide summary statistics.

Example:

```text
Endpoints Found: 24

GET: 8
POST: 6
PUT: 4
PATCH: 2
DELETE: 4

Protected Endpoints: 16
Public Endpoints: 8
```

---

# Validation Requirements

The inventory created in Phase 1 must be preserved until validation.

Phase 4 must compare:

Original Inventory

vs

Refactored Inventory

Verification:

✓ Route preserved

✓ Method preserved

✓ Authentication preserved

✓ Response contract preserved

✓ Status code preserved

---

# Failure Conditions

Validation must fail if:

* Route removed
* Route renamed
* HTTP method changed
* Authentication removed unexpectedly
* Response contract changed
* Endpoint no longer exists

Example:

Before:

```text
GET /users/{id}
```

After:

```text
GET /user/{id}
```

Result:

```text
FAIL

Reason:
Route contract changed.
```

---

# Confidence Rules

HIGH

* Route explicitly defined.

MEDIUM

* Route partially inferred.

LOW

* Dynamic registration.
* Reflection-based registration.
* Insufficient evidence.

Always report confidence when route discovery is uncertain.

---

# Final Rule

The endpoint inventory is the authoritative contract of the application.

Refactoring must preserve this contract unless explicitly approved by the user.

Never modify public API behavior without confirmation.