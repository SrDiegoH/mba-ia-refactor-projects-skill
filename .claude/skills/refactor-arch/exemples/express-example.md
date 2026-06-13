# Express MVC Reference Example

## Legacy Structure

```text
src/
├── app.js
├── GodManager.js
├── utils.js
```

Problems:

- God Class
- SQL in Routes
- Business logic in endpoints
- Hardcoded configuration

---

## Target Structure

```text
src/
├── app.js
├── config/
│   └── config.js
├── routes/
│   ├── product.routes.js
│   ├── user.routes.js
│   └── order.routes.js
├── controllers/
│   ├── product.controller.js
│   ├── user.controller.js
│   └── order.controller.js
├── models/
│   ├── product.model.js
│   ├── user.model.js
│   └── order.model.js
├── services/
│   ├── auth.service.js
│   └── order.service.js
└── middlewares/
    └── error.middleware.js
```

---

# Example 1

## BEFORE

```javascript
app.post("/products", async (req, res) => {

  const body = req.body

  if(body.price < 0){
      return res.status(400).send()
  }

  await db.query(
    `INSERT INTO products(name)
     VALUES('${body.name}')`
  )

  res.send()
})
```

Problems:

- SQL Injection
- Validation in Route
- Persistence in Route

---

## AFTER

Route

```javascript
router.post(
    "/",
    ProductController.create
)
```

Controller

```javascript
class ProductController {

    static async create(req, res) {

        ProductService.validate(req.body)

        await ProductModel.create(req.body)

        return res.status(201).json({
            success: true
        })
    }
}
```

Model

```javascript
class ProductModel {

    static async create(data) {

        return db.query(
            `
            INSERT INTO products(name)
            VALUES($1)
            `,
            [data.name]
        )
    }
}
```

---

# Example 2

## BEFORE

```javascript
const SECRET_KEY = "abc123"
```

## AFTER

```javascript
const SECRET_KEY =
    process.env.SECRET_KEY
```

---

# Example 3

## BEFORE

```javascript
class GodManager {

    login() {}
    createProduct() {}
    createOrder() {}
    generateReport() {}
    deleteUser() {}
}
```

---

## AFTER

```javascript
UserController
ProductController
OrderController

UserModel
ProductModel
OrderModel

AuthService
ReportService
```

---

# Error Handling

Middleware

```javascript
function errorHandler(
    err,
    req,
    res,
    next
) {

    return res.status(500).json({
        error: err.message
    })
}
```

---

Expected Result

- Routes contain only routing
- Controllers contain orchestration
- Models contain persistence
- Services contain business rules
- Configuration externalized
- Centralized error handling