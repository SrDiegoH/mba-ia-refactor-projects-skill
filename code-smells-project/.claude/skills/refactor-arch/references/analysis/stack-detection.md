# Stack Detection

## Purpose

Identify the complete technology stack used by the project.

The detected stack will be used by:

* Architecture Analysis
* Anti-Pattern Detection
* MVC Refactoring
* Validation

Stack detection must be evidence-based.

Never assume technologies.

Always verify through source code, dependencies, configuration files and imports.

If a technology cannot be determined with confidence, report UNKNOWN.

---

# Detection Process

Execute the following steps in order.

---

# Step 1 - Detect Programming Language

Inspect:

* file extensions
* project structure
* dependency files

Examples:

```text
.py
```

Classification:

```text
Python
```

---

```text
.js
```

Classification:

```text
JavaScript
```

---

```text
.ts
```

Classification:

```text
TypeScript
```

---

```text
.java
```

Classification:

```text
Java
```

---

```text
.cs
```

Classification:

```text
C#
```

---

# Step 2 - Detect Package Manager

Inspect root files.

Python:

```text
requirements.txt
```

Result:

```text
pip
```

---

```text
pyproject.toml
```

Possible:

```text
poetry
uv
pip
```

Inspect contents.

---

Node.js:

```text
package-lock.json
```

Result:

```text
npm
```

---

```text
yarn.lock
```

Result:

```text
yarn
```

---

```text
pnpm-lock.yaml
```

Result:

```text
pnpm
```

---

# Step 3 - Detect Framework

Inspect:

* imports
* dependency files
* application entry points

---

## Python

### Flask

Examples:

```python
from flask import Flask
```

```python
import flask
```

Classification:

```text
Flask
```

---

### FastAPI

Examples:

```python
from fastapi import FastAPI
```

Classification:

```text
FastAPI
```

---

### Django

Examples:

```python
from django
```

Classification:

```text
Django
```

---

## Node.js

### Express

Examples:

```javascript
const express = require("express")
```

or

```javascript
import express from "express"
```

Classification:

```text
Express
```

---

### NestJS

Examples:

```typescript
@Module()
```

```typescript
@Controller()
```

Classification:

```text
NestJS
```

---

### Koa

Examples:

```javascript
const Koa = require("koa")
```

Classification:

```text
Koa
```

---

# Step 4 - Detect Database

Inspect:

* environment variables
* connection strings
* ORM configuration
* repository code

---

## SQLite

Indicators:

```python
sqlite3.connect(...)
```

```text
.sqlite
.db
```

---

## PostgreSQL

Indicators:

```text
postgres://
postgresql://
```

Libraries:

```python
psycopg2
```

```javascript
pg
```

---

## MySQL

Indicators:

```text
mysql://
```

Libraries:

```python
mysqlclient
```

```javascript
mysql2
```

---

## MongoDB

Indicators:

```text
mongodb://
```

Libraries:

```python
pymongo
```

```javascript
mongoose
```

---

## Redis

Indicators:

```python
redis.Redis(...)
```

```javascript
new Redis(...)
```

---

# Step 5 - Detect ORM

Inspect imports and dependencies.

---

## SQLAlchemy

Examples:

```python
from sqlalchemy import
```

Classification:

```text
SQLAlchemy
```

---

## Django ORM

Examples:

```python
models.Model
```

Classification:

```text
Django ORM
```

---

## Prisma

Examples:

```javascript
@prisma/client
```

Classification:

```text
Prisma
```

---

## Sequelize

Examples:

```javascript
sequelize
```

Classification:

```text
Sequelize
```

---

## TypeORM

Examples:

```typescript
@Entity()
```

Classification:

```text
TypeORM
```

---

## No ORM

If raw SQL is used:

Classification:

```text
No ORM
```

---

# Step 6 - Detect Runtime Components

Inspect:

* middleware
* schedulers
* background workers
* queues
* cache layers

Examples:

---

## Celery

```python
from celery import Celery
```

Classification:

```text
Celery
```

---

## RQ

```python
from rq import Queue
```

Classification:

```text
RQ
```

---

## BullMQ

```javascript
import { Queue } from "bullmq"
```

Classification:

```text
BullMQ
```

---

# Step 7 - Detect API Style

Determine the API style.

Possible values:

```text
REST
GraphQL
RPC
Mixed
Unknown
```

---

## REST

Indicators:

```text
GET
POST
PUT
DELETE
PATCH
```

Resource routes:

```text
/users
/orders
/products
```

---

## GraphQL

Indicators:

```javascript
ApolloServer
```

```graphql
type Query
```

---

# Step 8 - Detect Deployment Indicators

Inspect:

```text
Dockerfile
docker-compose.yml
render.yaml
vercel.json
Procfile
```

Possible classifications:

```text
Docker
Render
Railway
Vercel
Heroku
Unknown
```

---

# Step 9 - Detect Test Frameworks

Inspect dependencies.

Python:

```python
pytest
```

```python
unittest
```

---

Node:

```javascript
jest
```

```javascript
vitest
```

```javascript
mocha
```

---

# Confidence Rules

## HIGH

Direct evidence exists.

Examples:

* imports found
* dependency declared
* configuration present

---

## MEDIUM

Indirect evidence exists.

Examples:

* file names suggest usage
* configuration partially present

---

## LOW

Weak evidence.

Examples:

* references in comments
* inferred from structure

---

# Stack Detection Output

Always produce the following format.

```text
Language: Python

Framework: Flask

Package Manager: pip

Database: PostgreSQL

ORM: SQLAlchemy

API Style: REST

Background Jobs: Celery

Deployment: Render

Testing: pytest

Confidence: HIGH

Evidence:

- requirements.txt found
- Flask imports detected
- SQLAlchemy imports detected
- PostgreSQL connection string detected
```

---

# Validation Rules

Never infer framework from folder names.

Never infer database from model names.

Never infer ORM from architecture.

Use source code and dependencies as primary evidence.

When evidence conflicts:

Report the conflict.

Example:

```text
Database: PostgreSQL

Confidence: MEDIUM

Reason:

PostgreSQL connection string detected,
but SQLite configuration also exists.
```

---

# Final Rule

Stack detection is the foundation of all later phases.

When uncertain:

Prefer UNKNOWN over incorrect classification.