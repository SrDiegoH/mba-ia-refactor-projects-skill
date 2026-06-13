# Target MVC Architecture

## Models

Responsibilities:

- persistence
- entity mapping

Must NOT contain:

- HTTP
- routing

---

## Controllers

Responsibilities:

- orchestration
- use cases

Must NOT contain:

- SQL
- persistence

---

## Views / Routes

Responsibilities:

- receive requests
- return responses

Must NOT contain:

- business rules

---

## Config

All configuration must be externalized.

Examples:

.env

settings.py

config.js

---

## Error Handling

Centralized.

Examples:

middleware
global handlers