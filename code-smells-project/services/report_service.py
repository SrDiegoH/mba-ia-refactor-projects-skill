import models.order as order_model

LIMIAR_DESCONTO_ALTO = 10_000
LIMIAR_DESCONTO_MEDIO = 5_000
LIMIAR_DESCONTO_BAIXO = 1_000
PERC_DESCONTO_ALTO = 0.10
PERC_DESCONTO_MEDIO = 0.05
PERC_DESCONTO_BAIXO = 0.02


def get_sales_report():
    stats = order_model.get_order_stats()
    faturamento = stats["faturamento"]
    total_pedidos = stats["total"]

    if faturamento > LIMIAR_DESCONTO_ALTO:
        desconto = faturamento * PERC_DESCONTO_ALTO
    elif faturamento > LIMIAR_DESCONTO_MEDIO:
        desconto = faturamento * PERC_DESCONTO_MEDIO
    elif faturamento > LIMIAR_DESCONTO_BAIXO:
        desconto = faturamento * PERC_DESCONTO_BAIXO
    else:
        desconto = 0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": stats["pendentes"],
        "pedidos_aprovados": stats["aprovados"],
        "pedidos_cancelados": stats["cancelados"],
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0
    }
