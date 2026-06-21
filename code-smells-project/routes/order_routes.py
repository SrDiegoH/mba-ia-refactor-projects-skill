from flask import Blueprint
from controllers import order_controller

order_bp = Blueprint("orders", __name__)

order_bp.add_url_rule("/pedidos", "criar_pedido", order_controller.create_order, methods=["POST"])
order_bp.add_url_rule("/pedidos", "listar_todos_pedidos", order_controller.list_all_orders, methods=["GET"])
order_bp.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", order_controller.list_user_orders, methods=["GET"])
order_bp.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", order_controller.update_order_status, methods=["PUT"])
order_bp.add_url_rule("/relatorios/vendas", "relatorio_vendas", order_controller.sales_report, methods=["GET"])
