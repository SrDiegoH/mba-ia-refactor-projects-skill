import logging
from flask import jsonify
import models.health as health_model

logger = logging.getLogger(__name__)


def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })


def health_check():
    try:
        counts = health_model.get_health_stats()
        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": counts,
            "versao": "1.0.0"
        }), 200
    except Exception as e:
        logger.error("Health check falhou: %s", e)
        return jsonify({"status": "erro", "detalhes": str(e)}), 500
