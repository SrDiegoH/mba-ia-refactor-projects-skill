# Refactoring Playbook

## RP001

Problem:
Hardcoded Credential

Before:

SECRET_KEY="abc"

After:

SECRET_KEY=os.getenv("SECRET_KEY")

---

## RP002

Problem:
SQL Injection

Before:

query="SELECT * FROM users WHERE id="+id

After:

cursor.execute(
    "SELECT * FROM users WHERE id=?",
    (id,)
)

---

## RP003

Problem:
God Class

Before:

models.py

After:

models/
controllers/
services/

---

## RP004

Problem:
Business Logic in Controller

Before:

@app.route(...)

price = calc()

After:

controller.calculate_price()

---

## RP005

Problem:
Global State

Before:

db_connection = global

After:

request scoped connection

---

## RP006

Problem:
Plaintext Password

Before:

senha

After:

bcrypt.hashpw()

---

## RP007

Problem:
N+1 Query

Before:

for item:
    select

After:

JOIN

---

## RP008

Problem:
Missing Validation

Before:

request.json

After:

DTO
Schema Validation