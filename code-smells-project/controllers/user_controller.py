import logging
from flask import request, jsonify
import services.user_service as user_service

logger = logging.getLogger(__name__)


def list_users():
    try:
        usuarios = user_service.list_users()
        return jsonify({"dados": usuarios, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def get_user(id):
    try:
        usuario = user_service.get_user(id)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True}), 200
        return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def create_user():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400

        id = user_service.create_user(dados)
        logger.info("Usuário criado: %s", dados.get("email"))
        return jsonify({"dados": {"id": id}, "sucesso": True}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
