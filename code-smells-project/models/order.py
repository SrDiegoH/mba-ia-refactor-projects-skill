from config.database import get_db
import models.product as product_model


def _build_orders_from_rows(rows):
    """Constrói lista de pedidos com itens aninhados a partir de rows de JOIN."""
    orders = {}
    for row in rows:
        order_id = row["id"]
        if order_id not in orders:
            orders[order_id] = {
                "id": row["id"],
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": []
            }
        if row["produto_id"] is not None:
            orders[order_id]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] or "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"]
            })
    return list(orders.values())


_ORDERS_WITH_ITEMS_QUERY = """
    SELECT p.id, p.usuario_id, p.status, p.total, p.criado_em,
           ip.produto_id, ip.quantidade, ip.preco_unitario,
           pr.nome as produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = ip.produto_id
"""


def get_all_orders():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(_ORDERS_WITH_ITEMS_QUERY + " ORDER BY p.id")
    return _build_orders_from_rows(cursor.fetchall())


def get_orders_by_user(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(_ORDERS_WITH_ITEMS_QUERY + " WHERE p.usuario_id = ? ORDER BY p.id", (usuario_id,))
    return _build_orders_from_rows(cursor.fetchall())


def create_order(usuario_id, total):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total)
    )
    return cursor.lastrowid


def create_order_item(pedido_id, produto_id, quantidade, preco_unitario):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
        (pedido_id, produto_id, quantidade, preco_unitario)
    )


def create_order_with_items(usuario_id, total, produtos_validos):
    db = get_db()
    try:
        pedido_id = create_order(usuario_id, total)
        for produto, quantidade in produtos_validos:
            create_order_item(pedido_id, produto["id"], quantidade, produto["preco"])
            product_model.decrement_stock(produto["id"], quantidade)
        db.commit()
        return pedido_id
    except Exception:
        db.rollback()
        raise


def update_order_status(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (novo_status, pedido_id)
    )
    db.commit()
    return True


def get_order_stats():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            COALESCE(SUM(total), 0) as faturamento,
            COALESCE(SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END), 0) as pendentes,
            COALESCE(SUM(CASE WHEN status = 'aprovado' THEN 1 ELSE 0 END), 0) as aprovados,
            COALESCE(SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END), 0) as cancelados
        FROM pedidos
    """)
    row = cursor.fetchone()
    return {
        "total": row["total"],
        "faturamento": row["faturamento"],
        "pendentes": row["pendentes"],
        "aprovados": row["aprovados"],
        "cancelados": row["cancelados"]
    }
