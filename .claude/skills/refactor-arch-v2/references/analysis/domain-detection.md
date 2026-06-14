# Domain Detection

## Purpose

Determine the business domain of the application.

The purpose is to understand what business problem the software solves.

This information is used to:

* improve architecture analysis
* identify domain boundaries
* detect mixed responsibilities
* generate more accurate audit reports

Domain detection must be evidence-based.

Never invent a domain.

If confidence is insufficient, return UNKNOWN.

---

# Detection Process

Execute the following steps.

## Step 1 - Analyze Project Naming

Inspect:

* repository name
* root folder name
* package names
* module names

Examples:

```text id="c4vk8y"
ecommerce-api
```

Strong signal:

```text id="59mv9x"
E-COMMERCE
```

---

```text id="dkw8pm"
task-manager-api
```

Strong signal:

```text id="53dzqx"
TASK MANAGEMENT
```

---

## Step 2 - Analyze Domain Entities

Inspect:

* model names
* database tables
* ORM entities
* DTOs
* schemas

Examples:

```text id="1t4a8w"
User
Product
Order
Cart
Payment
```

Strong signal:

```text id="nmbo2v"
E-COMMERCE
```

---

```text id="6u7dxs"
Course
Lesson
Student
Enrollment
Certificate
```

Strong signal:

```text id="85zc16"
LMS
```

---

```text id="gsltl8"
Task
Project
Status
Comment
Assignee
```

Strong signal:

```text id="l5r0zn"
TASK MANAGEMENT
```

---

## Step 3 - Analyze Endpoints

Inspect routes.

Examples:

```text id="1ue3m3"
GET /products
POST /orders
GET /cart
```

Strong signal:

```text id="swuj6x"
E-COMMERCE
```

---

```text id="hxt7g7"
GET /courses
POST /enrollments
GET /lessons
```

Strong signal:

```text id="g0rbg8"
LMS
```

---

```text id="ik0iqs"
GET /tasks
POST /projects
PATCH /tasks/:id
```

Strong signal:

```text id="9z1tup"
TASK MANAGEMENT
```

---

## Step 4 - Analyze Business Logic

Inspect:

* service layer
* controllers
* use cases
* workflows

Look for:

* checkout flows
* inventory control
* enrollment flows
* task assignment
* scheduling
* billing

Business workflows often provide stronger evidence than names.

---

# Supported Domains

The following domains should be recognized when possible.

---

## E-COMMERCE

Indicators:

* Product
* Cart
* Order
* Payment
* Checkout
* Inventory
* SKU
* Customer

Typical Routes:

```text id="f8g97s"
/products
/orders
/cart
/payments
```

---

## LMS

Learning Management System

Indicators:

* Course
* Lesson
* Student
* Enrollment
* Certificate
* Quiz
* Module

Typical Routes:

```text id="u59efm"
/courses
/lessons
/enrollments
```

---

## TASK MANAGEMENT

Indicators:

* Task
* Project
* Board
* Status
* Comment
* Assignee

Typical Routes:

```text id="4bsvjz"
/tasks
/projects
/comments
```

---

## CRM

Customer Relationship Management

Indicators:

* Lead
* Contact
* Opportunity
* Customer
* Pipeline

Typical Routes:

```text id="otg3jb"
/leads
/customers
/opportunities
```

---

## FINANCIAL

Indicators:

* Account
* Transaction
* Asset
* Portfolio
* Balance
* Statement

Typical Routes:

```text id="o1f9ja"
/accounts
/transactions
/assets
```

---

## CONTENT MANAGEMENT

Indicators:

* Article
* Post
* Category
* Author
* Tag
* Comment

Typical Routes:

```text id="vxo6oq"
/posts
/articles
/categories
```

---

## AUTHENTICATION

Indicators:

* Login
* Session
* Token
* Refresh Token
* User Management

Typical Routes:

```text id="73eqsh"
/login
/logout
/register
/refresh
```

---

## API PLATFORM

Indicators:

* Gateway
* Proxy
* Integration
* Connector
* Webhook

Typical Routes:

```text id="49g4yc"
/integrations
/webhooks
/connectors
```

---

## DATA PROCESSING

Indicators:

* Crawler
* Scraper
* Pipeline
* ETL
* Processor
* Import

Typical Components:

```text id="3h7y34"
crawler
extractor
transformer
loader
```

---

## UNKNOWN

Use UNKNOWN when evidence is insufficient.

Never force classification.

---

# Confidence Calculation

Determine confidence level.

---

## HIGH

Multiple strong signals agree.

Examples:

* project name
* entities
* endpoints

all indicate the same domain.

---

## MEDIUM

Some evidence exists.

Examples:

* entities suggest a domain
* routes are generic

---

## LOW

Weak evidence.

Examples:

* utility project
* generic names
* insufficient business context

---

# Mixed Domains

Projects may contain more than one domain.

Example:

```text id="86sy6y"
Orders
Products
Courses
Enrollments
```

Report:

```text id="m2q4gq"
Domain: MIXED

Confidence: MEDIUM
```

Explain why.

---

# Domain Detection Output

Always use the following format.

```text id="rq56c9"
Domain: E-COMMERCE

Confidence: HIGH

Evidence:

- Entities: Product, Order, Cart
- Routes: /products, /orders
- Checkout workflow detected
```

---

# Validation Rules

Do not infer domain from a single file.

Do not infer domain from a single route.

Do not infer domain from comments.

Use source code as primary evidence.

Prefer entities and business workflows over folder names.

If confidence is LOW and evidence is weak:

Return:

```text id="y16ygx"
Domain: UNKNOWN

Confidence: LOW
```

This is preferred over an incorrect classification.