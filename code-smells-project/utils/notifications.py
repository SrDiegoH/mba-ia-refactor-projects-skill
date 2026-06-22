import logging

logger = logging.getLogger(__name__)


def notify_order_created(pedido_id, usuario_id):
    logger.info("NOTIFICAÇÃO EMAIL: Pedido %d criado para usuário %d", pedido_id, usuario_id)
    logger.info("NOTIFICAÇÃO SMS: Seu pedido foi recebido!")
    logger.info("NOTIFICAÇÃO PUSH: Novo pedido recebido pelo sistema")


def notify_status_changed(pedido_id, status):
    if status == "aprovado":
        logger.info("NOTIFICAÇÃO: Pedido %d aprovado. Preparar envio.", pedido_id)
    elif status == "cancelado":
        logger.info("NOTIFICAÇÃO: Pedido %d cancelado. Devolver estoque.", pedido_id)
