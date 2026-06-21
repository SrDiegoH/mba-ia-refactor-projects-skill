# Flask Architecture Analysis Example

## Purpose

This example demonstrates how the audit phase should analyze a typical Flask application and identify architectural issues before migration.

The objective is to identify:

* current architecture
* layer responsibilities
* architectural violations
* anti-patterns
* migration complexity

This example represents a common real-world Flask application.

---

# Input Project

## Structure

```text
project/
├── app.py
├── controllers/
│   └── user_controller.py
├── services/
│   └── user_service.py
├── models/
│   └── user_model.py
├── database/
│   └── db.py
└── routes/
    └── user_routes.py
```

---

# Route

File:

```text
routes/user_routes.py
```

```python
from flask import Blueprint
from controllers.user_controller import get_user

user_bp = Blueprint("users", __name__)

user_bp.route("/users/<int:user_id>")(get_user)
```

---

# Controller

File:

```text
controllers/user_controller.py
```

```python
from flask import jsonify
from models.user_model import User


def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    discount = (
        0.20
        if user.total_purchases > 1000
        else 0.10
    )

    return jsonify({
        "id": user.id,
        "name": user.name,
        "discount": discount
    })
```

---

# Service

File:

```text
services/user_service.py
```

```python
# Empty service layer

```

---

# Model

File:

```text
models/user_model.py
```

```python
from database.db import db


class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    total_purchases = db.Column(
        db.Float
    )
```

---

# Analysis

## Framework Detection

Detected Framework:

```text
Flask
```

Confidence:

```text
HIGH
```

Evidence:

```python
from flask import Blueprint
```

---

## Architecture Detection

Detected Architecture:

```text
PARTIAL_MVC
```

Confidence:

```text
HIGH
```

Reasoning:

* routes exist
* controllers exist
* models exist
* service layer exists physically
* service layer is unused
* business logic remains in controller

---

## Layer Analysis

### Routes

Responsibility:

```text
HTTP endpoint mapping
```

Status:

```text
COMPLIANT
```

Evidence:

Route only maps requests.

No business logic detected.

---

### Controllers

Responsibility:

```text
Request orchestration
```

Status:

```text
NON_COMPLIANT
```

Evidence:

Controller contains:

* database access
* business rules
* response construction

---

### Services

Responsibility:

```text
Business logic
```

Status:

```text
MISSING_USAGE
```

Evidence:

Service layer exists but is not used.

---

### Models

Responsibility:

```text
Persistence
```

Status:

```text
COMPLIANT
```

Evidence:

Model only defines persistence structure.

---

# Findings

## AP101 - Business Logic In Controller

Severity:

```text
HIGH
```

File:

```text
controllers/user_controller.py
```

Evidence:

```python
discount = (
    0.20
    if user.total_purchases > 1000
    else 0.10
)
```

Impact:

Business rules implemented inside controller.

Recommendation:

Move business logic to service layer.

---

## AP102 - Direct Database Access In Controller

Severity:

```text
HIGH
```

File:

```text
controllers/user_controller.py
```

Evidence:

```python
user = User.query.get(user_id)
```

Impact:

Controller coupled directly to persistence layer.

Recommendation:

Move persistence access to service layer.

---

## AP104 - Missing Service Layer Usage

Severity:

```text
HIGH
```

File:

```text
services/user_service.py
```

Evidence:

Service layer exists but contains no implementation.

Impact:

Architectural inconsistency.

Recommendation:

Move business workflows into services.

---

# Recommended Target Architecture

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Model
```

---

# Refactored Example

## Route

```python
from flask import Blueprint
from controllers.user_controller import get_user

user_bp = Blueprint("users", __name__)

user_bp.route("/users/<int:user_id>")(get_user)
```

---

## Controller

```python
from flask import jsonify
from services.user_service import get_user_data


def get_user(user_id):
    result = get_user_data(user_id)

    return jsonify(result)
```

---

## Service

```python
from models.user_model import User


def get_user_data(user_id):
    user = User.query.get(user_id)

    if not user:
        raise ValueError(
            "User not found"
        )

    discount = (
        0.20
        if user.total_purchases > 1000
        else 0.10
    )

    return {
        "id": user.id,
        "name": user.name,
        "discount": discount
    }
```

---

## Model

```python
from database.db import db


class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    total_purchases = db.Column(
        db.Float
    )
```

---

# Migration Complexity

Estimated Complexity:

```text
LOW
```

Reason:

* MVC structure already partially exists
* routes are already separated
* models are already separated
* business logic extraction is straightforward

---

# Audit Summary

```text
Architecture: PARTIAL_MVC

Critical Findings: 0
High Findings: 3
Medium Findings: 0
Low Findings: 0

Migration Readiness:
REQUIRES_REVIEW
```

---

# Key Takeaway

The existence of folders named:

* routes
* controllers
* services
* models

does not prove correct MVC implementation.

Architectural classification must be based on actual responsibilities implemented in code.

Folder structure alone is insufficient evidence.

All architectural findings must be supported by implementation evidence.