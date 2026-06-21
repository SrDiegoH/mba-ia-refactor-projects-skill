import logging
from config.database import get_db
import models.order as order_model

logger = logging.getLogger(__name__)

STATUSES_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]


def create_order(usuario_id, itens):
    if not itens:
        raise ValueError("Pedido deve ter pelo menos 1 item")

    db = get_db()
    try:
        total = 0
        produtos_validos = []
        for item in itens:
            produto = order_model.get_product_for_order(item["produto_id"])
            if produto is None:
                raise ValueError(f"Produto {item['produto_id']} não encontrado")
            if produto["estoque"] < item["quantidade"]:
                raise ValueError(f"Estoque insuficiente para {produto['nome']}")
            total += produto["preco"] * item["quantidade"]
            produtos_validos.append((produto, item["quantidade"]))

        pedido_id = order_model.create_order(usuario_id, total)

        for produto, quantidade in produtos_validos:
            order_model.create_order_item(pedido_id, produto["id"], quantidade, produto["preco"])
            order_model.decrement_stock(produto["id"], quantidade)

        db.commit()
        _notify_order_created(pedido_id, usuario_id)
        return {"pedido_id": pedido_id, "total": total}

    except Exception:
        db.rollback()
        raise


def list_orders():
    return order_model.get_all_orders()


def get_user_orders(usuario_id):
    return order_model.get_orders_by_user(usuario_id)


def update_order_status(pedido_id, novo_status):
    if novo_status not in STATUSES_VALIDOS:
        raise ValueError("Status inválido")
    order_model.update_order_status(pedido_id, novo_status)
    _notify_status_changed(pedido_id, novo_status)
    return True


def _notify_order_created(pedido_id, usuario_id):
    logger.info("NOTIFICAÇÃO EMAIL: Pedido %d criado para usuário %d", pedido_id, usuario_id)
    logger.info("NOTIFICAÇÃO SMS: Seu pedido foi recebido!")
    logger.info("NOTIFICAÇÃO PUSH: Novo pedido recebido pelo sistema")


def _notify_status_changed(pedido_id, status):
    if status == "aprovado":
        logger.info("NOTIFICAÇÃO: Pedido %d aprovado. Preparar envio.", pedido_id)
    elif status == "cancelado":
        logger.info("NOTIFICAÇÃO: Pedido %d cancelado. Devolver estoque.", pedido_id)
