from flask import Blueprint
from controllers import user_controller

user_bp = Blueprint("users", __name__)

user_bp.add_url_rule("/usuarios", "listar_usuarios", user_controller.list_users, methods=["GET"])
user_bp.add_url_rule("/usuarios/<int:id>", "buscar_usuario", user_controller.get_user, methods=["GET"])
user_bp.add_url_rule("/usuarios", "criar_usuario", user_controller.create_user, methods=["POST"])
