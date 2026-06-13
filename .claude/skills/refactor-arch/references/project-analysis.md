# Project Analysis Heuristics

## Language Detection

Python:
- requirements.txt
- pyproject.toml
- *.py

Node:
- package.json
- *.js
- *.ts

Java:
- pom.xml
- build.gradle

## Framework Detection

Flask:
from flask import

FastAPI:
from fastapi import

Express:
require("express")

NestJS:
@Module

Spring:
@SpringBootApplication

## Database Detection

SQLite:
sqlite3

PostgreSQL:
psycopg2
postgres

MySQL:
mysql
mysql2

MongoDB:
mongoose
mongodb

## Architecture Detection

Monolith

Signals:

- Few large files
- Mixed responsibilities

MVC

Signals:

- models/
- controllers/
- routes/

Layered

Signals:

- services/
- repositories/

## Domain Detection

Infer from:

- routes
- tables
- entities

Examples:

produto -> ecommerce
pedido -> ecommerce

task -> task manager

curso -> LMS