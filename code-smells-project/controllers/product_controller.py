import logging
from flask import request, jsonify
import services.product_service as product_service

logger = logging.getLogger(__name__)


def list_products():
    try:
        produtos = product_service.list_products()
        logger.info("Listando %d produtos", len(produtos))
        return jsonify({"dados": produtos, "sucesso": True}), 200
    except Exception as e:
        logger.error("Erro ao listar produtos: %s", e)
        return jsonify({"erro": str(e)}), 500


def get_product(id):
    try:
        produto = product_service.get_product(id)
        if produto:
            return jsonify({"dados": produto, "sucesso": True}), 200
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def create_product():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        for campo in ["nome", "preco", "estoque"]:
            if campo not in dados:
                return jsonify({"erro": f"{campo.capitalize()} é obrigatório"}), 400

        id = product_service.create_product(dados)
        logger.info("Produto criado com ID: %d", id)
        return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.error("Erro ao criar produto: %s", e)
        return jsonify({"erro": str(e)}), 500


def update_product(id):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        for campo in ["nome", "preco", "estoque"]:
            if campo not in dados:
                return jsonify({"erro": f"{campo.capitalize()} é obrigatório"}), 400

        result = product_service.update_product(id, dados)
        if result is None:
            return jsonify({"erro": "Produto não encontrado"}), 404
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def delete_product(id):
    try:
        result = product_service.delete_product(id)
        if result is None:
            return jsonify({"erro": "Produto não encontrado"}), 404
        logger.info("Produto %d deletado", id)
        return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def search_products():
    try:
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria", None)
        preco_min = request.args.get("preco_min", None)
        preco_max = request.args.get("preco_max", None)

        if preco_min:
            preco_min = float(preco_min)
        if preco_max:
            preco_max = float(preco_max)

        resultados = product_service.search_products(termo, categoria, preco_min, preco_max)
        return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
