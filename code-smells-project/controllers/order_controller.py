import logging
from flask import request, jsonify
import services.order_service as order_service
import services.report_service as report_service

logger = logging.getLogger(__name__)


def create_order():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400

        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])

        if not usuario_id:
            return jsonify({"erro": "Usuario ID é obrigatório"}), 400

        resultado = order_service.create_order(usuario_id, itens)
        return jsonify({"dados": resultado, "sucesso": True, "mensagem": "Pedido criado com sucesso"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e), "sucesso": False}), 400
    except Exception as e:
        logger.error("Erro crítico ao criar pedido: %s", e)
        return jsonify({"erro": str(e)}), 500


def list_all_orders():
    try:
        pedidos = order_service.list_orders()
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def list_user_orders(usuario_id):
    try:
        pedidos = order_service.get_user_orders(usuario_id)
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def update_order_status(pedido_id):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        novo_status = dados.get("status", "")
        order_service.update_order_status(pedido_id, novo_status)
        return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


def sales_report():
    try:
        relatorio = report_service.get_sales_report()
        return jsonify({"dados": relatorio, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
