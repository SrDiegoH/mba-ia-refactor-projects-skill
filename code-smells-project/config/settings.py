import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-in-production")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
