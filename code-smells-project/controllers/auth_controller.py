import logging
from flask import request, jsonify
import services.auth_service as auth_service

logger = logging.getLogger(__name__)


def login():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400

        email = dados.get("email", "")
        senha = dados.get("senha", "")

        usuario = auth_service.login(email, senha)
        if usuario:
            logger.info("Login bem-sucedido: %s", email)
            return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200

        logger.warning("Login falhou: %s", email)
        return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
