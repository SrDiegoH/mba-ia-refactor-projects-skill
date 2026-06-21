# MVC Target Architecture

## Purpose

Define the target architecture that should exist after refactoring.

The purpose of this document is to provide a consistent architectural destination for all projects.

This document does not define responsibilities.

Responsibilities are defined in:

```text
mvc-rules.md
```

This document defines structure only.

---

# Architecture Goals

The target architecture must:

* Separate concerns
* Improve maintainability
* Improve testability
* Reduce coupling
* Improve readability
* Preserve application behavior

Refactoring must improve structure without changing business functionality.

---

# Canonical MVC Structure

The preferred structure is:

```text
src/
├── config/
├── controllers/
├── services/
├── models/
├── routes/
├── middleware/
├── utils/
├── tests/
└── app
```

Framework-specific variations are acceptable.

Responsibilities must remain unchanged.

---

# Layer Overview

```text
HTTP Request
      │
      ▼
 Routes
      │
      ▼
Controllers
      │
      ▼
 Services
      │
      ▼
  Models
      │
      ▼
 Database
```

Dependency direction must always flow downward.

---

# Required Directories

The following directories should exist whenever applicable.

---

## config/

Purpose:

Centralized application configuration.

Examples:

```text
config/
├── settings.py
├── database.py
└── logging.py
```

Possible Contents:

* environment variables
* application settings
* database configuration
* cache configuration
* logging configuration

---

## controllers/

Purpose:

Request orchestration.

Examples:

```text
controllers/
├── user_controller.py
├── order_controller.py
└── auth_controller.py
```

Controllers should be thin.

---

## services/

Purpose:

Business logic.

Examples:

```text
services/
├── user_service.py
├── order_service.py
└── payment_service.py
```

Services should contain:

* business rules
* workflows
* use cases

---

## models/

Purpose:

Persistence and domain entities.

Examples:

```text
models/
├── user.py
├── order.py
└── product.py
```

Possible Contents:

* ORM entities
* repositories
* persistence models

---

## routes/

Purpose:

Endpoint registration.

Examples:

```text
routes/
├── user_routes.py
├── order_routes.py
└── auth_routes.py
```

Routes should only map URLs to controllers.

---

## middleware/

Purpose:

Cross-cutting concerns.

Examples:

```text
middleware/
├── auth.py
├── logging.py
└── rate_limit.py
```

Possible Contents:

* authentication
* authorization
* logging
* tracing
* request filters

---

## utils/

Purpose:

Reusable technical helpers.

Examples:

```text
utils/
├── dates.py
├── strings.py
└── serializers.py
```

Must not contain business rules.

---

## tests/

Purpose:

Automated tests.

Examples:

```text
tests/
├── test_users.py
├── test_orders.py
└── test_auth.py
```

May be omitted if project contains no tests.

---

# Python Target Structure

## Flask

Preferred structure:

```text
src/
├── app.py
├── config/
│
├── routes/
│   ├── user_routes.py
│   └── order_routes.py
│
├── controllers/
│   ├── user_controller.py
│   └── order_controller.py
│
├── services/
│   ├── user_service.py
│   └── order_service.py
│
├── models/
│   ├── user.py
│   └── order.py
│
├── middleware/
│
├── utils/
│
└── tests/
```

---

## FastAPI

Preferred structure:

```text
src/
├── main.py
├── config/
├── routes/
├── controllers/
├── services/
├── models/
├── middleware/
├── utils/
└── tests/
```

---

# Node.js Target Structure

## Express

Preferred structure:

```text
src/
├── app.js
│
├── config/
│
├── routes/
│   ├── user.routes.js
│   └── order.routes.js
│
├── controllers/
│   ├── user.controller.js
│   └── order.controller.js
│
├── services/
│   ├── user.service.js
│   └── order.service.js
│
├── models/
│   ├── user.model.js
│   └── order.model.js
│
├── middleware/
│
├── utils/
│
└── tests/
```

---

# Existing Architecture Preservation

Not every project requires a complete rewrite.

---

## Monolithic Project

Example:

```text
app.py
```

Migration:

```text
Full MVC Migration
```

---

## Partial MVC Project

Example:

```text
models/
routes/
services/
```

Migration:

```text
Incremental Migration
```

Preserve existing structure whenever possible.

---

## Existing MVC Project

Migration:

```text
Targeted Improvements Only
```

Avoid unnecessary reorganization.

---

# Naming Conventions

Controllers:

```text
user_controller.py
order_controller.py
```

or

```text
user.controller.js
order.controller.js
```

---

Services:

```text
user_service.py
order_service.py
```

or

```text
user.service.js
order.service.js
```

---

Routes:

```text
user_routes.py
order_routes.py
```

or

```text
user.routes.js
order.routes.js
```

---

Models:

```text
user.py
order.py
```

or

```text
user.model.js
order.model.js
```

---

# Optional Directories

These may exist when justified.

---

## repositories/

```text
repositories/
├── user_repository.py
└── order_repository.py
```

Useful for:

* complex persistence
* repository pattern

---

## dto/

```text
dto/
├── user_dto.py
└── order_dto.py
```

Useful for:

* API contracts
* request mapping

---

## exceptions/

```text
exceptions/
├── business_exception.py
└── validation_exception.py
```

Useful for:

* centralized error handling

---

# Validation Criteria

The architecture is considered MVC compliant when:

✓ Routes register endpoints

✓ Controllers orchestrate requests

✓ Services contain business logic

✓ Models contain persistence logic

✓ Configuration centralized

✓ Dependency direction respected

---

# Non-Goals

The following are NOT required:

* Repository Pattern
* CQRS
* Event Sourcing
* Clean Architecture
* Hexagonal Architecture
* Domain Driven Design

These patterns may exist but are not required.

---

# Migration Principle

Prefer:

```text
Move Code
```

over:

```text
Rewrite Code
```

Preserve behavior whenever possible.

---

# Final Rule

The target architecture is defined by responsibilities, not folder names.

A project is considered MVC-compliant only when responsibilities are correctly separated according to mvc-rules.md.