import logging
import models.order as order_model
import models.product as product_model
import utils.notifications as notifications

logger = logging.getLogger(__name__)

STATUSES_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]


def create_order(usuario_id, itens):
    if not itens:
        raise ValueError("Pedido deve ter pelo menos 1 item")

    total = 0
    produtos_validos = []
    for item in itens:
        produto = product_model.get_product_for_order(item["produto_id"])
        if produto is None:
            raise ValueError(f"Produto {item['produto_id']} não encontrado")
        if produto["estoque"] < item["quantidade"]:
            raise ValueError(f"Estoque insuficiente para {produto['nome']}")
        total += produto["preco"] * item["quantidade"]
        produtos_validos.append((produto, item["quantidade"]))

    pedido_id = order_model.create_order_with_items(usuario_id, total, produtos_validos)
    notifications.notify_order_created(pedido_id, usuario_id)
    return {"pedido_id": pedido_id, "total": total}


def list_orders():
    return order_model.get_all_orders()


def get_user_orders(usuario_id):
    return order_model.get_orders_by_user(usuario_id)


def update_order_status(pedido_id, novo_status):
    if novo_status not in STATUSES_VALIDOS:
        raise ValueError("Status inválido")
    order_model.update_order_status(pedido_id, novo_status)
    notifications.notify_status_changed(pedido_id, novo_status)
    return True
