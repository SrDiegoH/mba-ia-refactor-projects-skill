from flask import Blueprint
from controllers import product_controller

product_bp = Blueprint("products", __name__)

product_bp.add_url_rule("/produtos", "listar_produtos", product_controller.list_products, methods=["GET"])
product_bp.add_url_rule("/produtos/busca", "buscar_produtos", product_controller.search_products, methods=["GET"])
product_bp.add_url_rule("/produtos/<int:id>", "buscar_produto", product_controller.get_product, methods=["GET"])
product_bp.add_url_rule("/produtos", "criar_produto", product_controller.create_product, methods=["POST"])
product_bp.add_url_rule("/produtos/<int:id>", "atualizar_produto", product_controller.update_product, methods=["PUT"])
product_bp.add_url_rule("/produtos/<int:id>", "deletar_produto", product_controller.delete_product, methods=["DELETE"])
