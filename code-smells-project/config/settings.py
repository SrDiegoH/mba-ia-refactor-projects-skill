import os
import warnings

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "dev-secret-key-change-in-production"
    warnings.warn(
        "SECRET_KEY não definido — usando valor inseguro de desenvolvimento",
        stacklevel=1
    )
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
