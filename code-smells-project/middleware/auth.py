import os
import functools
import warnings
from flask import request, jsonify

_ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
if not _ADMIN_TOKEN:
    _ADMIN_TOKEN = "admin-dev-token"
    warnings.warn(
        "ADMIN_TOKEN não definido — usando token inseguro de desenvolvimento",
        stacklevel=1
    )


def require_admin(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-Admin-Token")
        if not token or token != _ADMIN_TOKEN:
            return jsonify({"erro": "Acesso não autorizado", "sucesso": False}), 401
        return f(*args, **kwargs)
    return decorated
