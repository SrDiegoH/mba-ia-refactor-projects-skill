# Express.js Architecture Analysis Example

## Purpose

This example demonstrates how the audit phase should analyze a typical Express.js application and identify architectural issues before migration.

The objective is to identify:

* current architecture
* layer responsibilities
* architectural violations
* anti-patterns
* migration complexity

This example represents a common real-world Express application.

---

# Input Project

## Structure

```text
project/
├── app.js
├── routes/
│   └── userRoutes.js
├── controllers/
│   └── userController.js
├── services/
│   └── userService.js
├── models/
│   └── userModel.js
└── config/
    └── database.js
```

---

# Route

File:

```text
routes/userRoutes.js
```

```javascript
const express = require('express')
const router = express.Router()
const userController = require('../controllers/userController')

router.get('/:id', userController.getUser)

module.exports = router
```

---

# Controller

File:

```text
controllers/userController.js
```

```javascript
const User = require('../models/userModel')

exports.getUser = async (req, res) => {
    const user = await User.findByPk(req.params.id)

    if (!user) {
        return res.status(404).json({
            error: 'User not found'
        })
    }

    const discount =
        user.totalPurchases > 1000
            ? 0.20
            : 0.10

    return res.json({
        id: user.id,
        name: user.name,
        discount
    })
}
```

---

# Service

File:

```text
services/userService.js
```

```javascript
module.exports = {}
```

---

# Model

File:

```text
models/userModel.js
```

```javascript
const { DataTypes } = require('sequelize')
const sequelize = require('../config/database')

module.exports = sequelize.define('User', {
    name: DataTypes.STRING,
    totalPurchases: DataTypes.FLOAT
})
```

---

# Analysis

## Framework Detection

Detected Framework:

```text
Express.js
```

Confidence:

```text
HIGH
```

Evidence:

```javascript
const express = require('express')
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

Controllers exist.

Models exist.

Routes exist.

Service layer exists physically but is not used.

Business logic remains inside controllers.

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

Reason:

Contains business rules.

Contains discount calculation.

Contains persistence access.

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

Reason:

Service layer exists but is unused.

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

---

# Findings

## AP101 - Business Logic In Controller

Severity:

```text
HIGH
```

File:

```text
controllers/userController.js
```

Evidence:

```javascript
const discount =
    user.totalPurchases > 1000
        ? 0.20
        : 0.10
```

Impact:

Business rules implemented inside controller.

Recommendation:

Move logic to service layer.

---

## AP102 - Direct Database Access In Controller

Severity:

```text
HIGH
```

File:

```text
controllers/userController.js
```

Evidence:

```javascript
const user = await User.findByPk(req.params.id)
```

Impact:

Controller coupled to persistence layer.

Recommendation:

Move database access into service or repository layer.

---

## AP104 - Missing Service Layer Usage

Severity:

```text
HIGH
```

File:

```text
services/userService.js
```

Evidence:

Service exists but is not used.

Impact:

Architectural inconsistency.

Recommendation:

Move business rules into service layer.

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

```javascript
router.get('/:id', userController.getUser)
```

---

## Controller

```javascript
const userService = require('../services/userService')

exports.getUser = async (req, res) => {
    const result = await userService.getUser(
        req.params.id
    )

    return res.json(result)
}
```

---

## Service

```javascript
const User = require('../models/userModel')

async function getUser(id) {
    const user = await User.findByPk(id)

    if (!user) {
        throw new Error('User not found')
    }

    const discount =
        user.totalPurchases > 1000
            ? 0.20
            : 0.10

    return {
        id: user.id,
        name: user.name,
        discount
    }
}

module.exports = {
    getUser
}
```

---

# Migration Complexity

Estimated Complexity:

```text
LOW
```

Reason:

* MVC structure already exists
* service layer already exists
* limited business logic extraction required

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

* controllers
* services
* models

does not prove correct MVC implementation.

Layer responsibilities must be validated through implementation analysis.

Architectural classification must be based on code behavior, not project structure.