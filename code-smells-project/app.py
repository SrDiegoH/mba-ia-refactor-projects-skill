import logging
from flask import Flask
from flask_cors import CORS
from config.settings import SECRET_KEY, DEBUG
from config.database import get_db
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp
from routes.auth_routes import auth_bp
from routes.system_routes import system_bp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG
CORS(app)

app.register_blueprint(product_bp)
app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(system_bp)

if __name__ == "__main__":
    get_db()
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print("Rodando em http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
