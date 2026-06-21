# Endpoint Validation

## Purpose

Define the validation process used to verify that all application endpoints continue to function correctly after refactoring.

Endpoint validation ensures that architectural changes do not alter:

* endpoint availability
* route registration
* HTTP methods
* request contracts
* response contracts
* status codes

Endpoint validation occurs after:

```text
Boot Validation
Architecture Validation
```

and before:

```text
Behavioral Validation
```

---

# Validation Principles

## Preserve Public Contracts

Refactoring must not change public APIs.

The following must remain unchanged unless explicitly requested:

* URLs
* HTTP methods
* request parameters
* request body schema
* response schema
* response status codes

---

## Validate Every Endpoint

Every endpoint discovered during analysis must be validated.

Reference:

```text
endpoint-inventory.md
```

The inventory created during audit becomes the source of truth.

---

## Evidence Required

Endpoint validation must be evidence-based.

Do not assume endpoint availability because:

* routes exist
* controllers exist
* application boots

Verification is required.

---

# Validation Workflow

## Step 1 - Load Endpoint Inventory

Retrieve endpoint inventory generated during audit.

Reference:

```text
endpoint-inventory.md
```

Example:

```text
GET     /users
GET     /users/{id}
POST    /users
PUT     /users/{id}
DELETE  /users/{id}
```

This becomes the validation baseline.

---

## Step 2 - Verify Endpoint Registration

Confirm all inventoried endpoints remain registered.

Verify:

* path exists
* HTTP method exists
* route is reachable

Example:

Before:

```text
GET /users/{id}
```

After:

```text
GET /users/{id}
```

Result:

```text
PASS
```

---

## Step 3 - Verify HTTP Methods

Confirm method preservation.

Example:

Before:

```text
POST /users
```

After:

```text
POST /users
```

Result:

```text
PASS
```

Failure Example:

Before:

```text
POST /users
```

After:

```text
PUT /users
```

Result:

```text
FAIL
```

---

## Step 4 - Verify Request Contracts

Validate:

* path parameters
* query parameters
* headers
* request body schema

Example:

Before:

```json
{
  "name": "John"
}
```

After:

```json
{
  "name": "John"
}
```

Result:

```text
PASS
```

Failure Example:

Before:

```json
{
  "name": "John"
}
```

After:

```json
{
  "name": "John",
  "status": "active"
}
```

Result:

```text
FAIL
```

Reason:

New required field introduced.

---

## Step 5 - Verify Response Contracts

Validate:

* field names
* field types
* structure
* nesting

Example:

Before:

```json
{
  "id": 1,
  "name": "John"
}
```

After:

```json
{
  "id": 1,
  "name": "John"
}
```

Result:

```text
PASS
```

Failure Example:

Before:

```json
{
  "id": 1,
  "name": "John"
}
```

After:

```json
{
  "user_id": 1,
  "name": "John"
}
```

Result:

```text
FAIL
```

Reason:

Contract changed.

---

## Step 6 - Verify Status Codes

Validate status code behavior.

Example:

Before:

```http
200 OK
```

After:

```http
200 OK
```

Result:

```text
PASS
```

Failure Example:

Before:

```http
404 Not Found
```

After:

```http
500 Internal Server Error
```

Result:

```text
FAIL
```

---

## Step 7 - Verify Error Responses

Validate:

* error payload structure
* status codes
* expected messages

Example:

Before:

```json
{
  "error": "User not found"
}
```

After:

```json
{
  "error": "User not found"
}
```

Result:

```text
PASS
```

Failure Example:

Before:

```json
{
  "error": "User not found"
}
```

After:

```json
{
  "message": "Not found"
}
```

Result:

```text
FAIL
```

---

# Validation Rules

## EV001 - Endpoint Exists

Verify:

Endpoint remains registered.

Status:

```text
PASS
```

or

```text
FAIL
```

---

## EV002 - HTTP Method Preserved

Verify:

Original HTTP method remains unchanged.

Status:

```text
PASS
```

or

```text
FAIL
```

---

## EV003 - Path Preserved

Verify:

Endpoint path remains unchanged.

Status:

```text
PASS
```

or

```text
FAIL
```

Failure Example:

Before:

```text
/users/{id}
```

After:

```text
/api/users/{id}
```

---

## EV004 - Path Parameters Preserved

Verify:

Path parameter names and semantics remain unchanged.

Example:

Before:

```text
/users/{id}
```

After:

```text
/users/{id}
```

Pass.

Failure:

```text
/users/{userId}
```

without contract compatibility validation.

---

## EV005 - Query Parameters Preserved

Verify:

Query parameters remain compatible.

Example:

Before:

```text
/users?page=1
```

After:

```text
/users?page=1
```

Pass.

---

## EV006 - Request Schema Preserved

Verify:

Request payload schema remains unchanged.

Status:

```text
PASS
```

or

```text
FAIL
```

---

## EV007 - Response Schema Preserved

Verify:

Response payload schema remains unchanged.

Status:

```text
PASS
```

or

```text
FAIL
```

---

## EV008 - Response Types Preserved

Verify:

Field types remain unchanged.

Example:

Before:

```json
{
  "id": 1
}
```

After:

```json
{
  "id": "1"
}
```

Result:

```text
FAIL
```

---

## EV009 - Status Codes Preserved

Verify:

Status codes remain unchanged.

Status:

```text
PASS
```

or

```text
FAIL
```

---

## EV010 - Error Contract Preserved

Verify:

Error responses remain compatible.

Status:

```text
PASS
```

or

```text
FAIL
```

---

## EV011 - Authentication Requirements Preserved

Verify:

Authentication behavior remains unchanged.

Examples:

Before:

```text
Requires JWT
```

After:

```text
Requires JWT
```

Pass.

Failure:

Authentication removed.

---

## EV012 - Authorization Requirements Preserved

Verify:

Permissions remain unchanged.

Examples:

Before:

```text
Admin Only
```

After:

```text
Admin Only
```

Pass.

Failure:

Permission requirements changed.

---

# Endpoint Status Classification

## PASS

Conditions:

```text
Endpoint fully compatible.
```

All validation rules pass.

---

## PARTIAL_PASS

Conditions:

```text
Minor differences detected.
```

No contract breakage.

No behavioral impact.

Requires review.

---

## FAIL

Conditions:

```text
Contract changed.
```

Examples:

* path changed
* method changed
* schema changed
* status codes changed
* endpoint missing

---

# Validation Report Format

Example:

```text
Endpoint:
GET /users/{id}

EV001 - PASS
Endpoint Exists

EV002 - PASS
Method Preserved

EV003 - PASS
Path Preserved

EV004 - PASS
Parameters Preserved

EV006 - PASS
Request Schema Preserved

EV007 - PASS
Response Schema Preserved

EV009 - PASS
Status Codes Preserved

Result:
PASS
```

---

# Missing Endpoint Rules

If an endpoint existed during audit but no longer exists:

Status:

```text
FAIL
```

Example:

Before:

```text
GET /users/{id}
```

After:

```text
Endpoint Missing
```

Migration Status:

```text
NOT_READY
```

---

# Contract Drift Rules

Any of the following constitute contract drift:

* renamed fields
* removed fields
* added required fields
* changed types
* changed status codes
* changed authentication requirements

Contract drift is considered a failure unless explicitly requested.

---

# Relationship To Other Validation Phases

Validation sequence:

```text
1. Boot Validation
2. Architecture Validation
3. Endpoint Validation
4. Behavioral Validation
5. Modernization Validation
```

Endpoint validation depends on successful boot validation.

---

# Escalation Rules

If validation detects:

* missing endpoint
* changed request schema
* changed response schema
* changed authentication behavior
* changed authorization behavior

Status:

```text
REQUIRES_HUMAN_REVIEW
```

Migration must stop until reviewed.

---

# Completion Criteria

Endpoint validation is considered successful when:

* all inventoried endpoints exist
* all methods match
* all paths match
* all contracts match
* all status codes match
* authentication behavior matches
* authorization behavior matches

---

# Final Rule

Architectural refactoring must be invisible to API consumers.

If a client application must change to work with the refactored system, endpoint validation has failed.