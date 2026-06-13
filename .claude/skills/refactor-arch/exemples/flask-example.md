# Flask MVC Reference Example

## Legacy Structure

```text
app.py
models.py
database.py
controllers.py
```

Problems:

- SQL mixed with routes
- Business rules inside endpoints
- Global database connection
- Hardcoded configuration

---

## Target Structure

```text
src/
├── app.py
├── config/
│   └── settings.py
├── models/
│   ├── product_model.py
│   ├── user_model.py
│   └── order_model.py
├── controllers/
│   ├── product_controller.py
│   ├── user_controller.py
│   └── order_controller.py
├── routes/
│   ├── product_routes.py
│   ├── user_routes.py
│   └── order_routes.py
├── services/
│   ├── auth_service.py
│   └── order_service.py
└── middlewares/
    └── error_handler.py
```

---

# Example 1

## BEFORE

```python
@app.route("/products", methods=["POST"])
def create_product():

    data = request.json

    if data["price"] < 0:
        return {"error": "invalid"}

    conn = get_connection()

    conn.execute(
        f"""
        INSERT INTO products
        VALUES ('{data["name"]}')
        """
    )

    return {"ok": True}
```

Problems:

- SQL Injection
- Validation in Route
- Persistence in Route

---

## AFTER

Route

```python
@product_bp.route("/", methods=["POST"])
def create_product():
    return ProductController.create()
```

Controller

```python
class ProductController:

    @staticmethod
    def create():

        payload = request.json

        ProductService.validate(payload)

        ProductModel.create(payload)

        return {"success": True}, 201
```

Model

```python
class ProductModel:

    @staticmethod
    def create(data):

        cursor.execute(
            """
            INSERT INTO products(name)
            VALUES (?)
            """,
            (data["name"],)
        )
```

---

# Example 2

## BEFORE

```python
app.config["SECRET_KEY"] = "123456"
```

## AFTER

settings.py

```python
import os

SECRET_KEY = os.getenv("SECRET_KEY")
```

app.py

```python
from config.settings import SECRET_KEY

app.config["SECRET_KEY"] = SECRET_KEY
```

---

# Example 3

## BEFORE

```python
db_connection = sqlite3.connect(...)
```

## AFTER

```python
def get_connection():

    conn = sqlite3.connect(DB_PATH)

    try:
        yield conn

    finally:
        conn.close()
```

---

Expected Result

- Routes only handle HTTP
- Controllers orchestrate flow
- Models handle persistence
- Config isolated
- Error handling centralized