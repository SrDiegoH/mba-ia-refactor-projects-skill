import models.product as product_model

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]


def list_products():
    return product_model.get_all_products()


def get_product(id):
    return product_model.get_product_by_id(id)


def create_product(dados):
    nome = dados.get("nome", "")
    descricao = dados.get("descricao", "")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    categoria = dados.get("categoria", "geral")

    if not nome or len(nome) < 2:
        raise ValueError("Nome inválido (mínimo 2 caracteres)")
    if len(nome) > 200:
        raise ValueError("Nome muito longo (máximo 200 caracteres)")
    if preco is None or preco < 0:
        raise ValueError("Preço não pode ser negativo")
    if estoque is None or estoque < 0:
        raise ValueError("Estoque não pode ser negativo")
    if categoria not in CATEGORIAS_VALIDAS:
        raise ValueError(f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}")

    return product_model.create_product(nome, descricao, preco, estoque, categoria)


def update_product(id, dados):
    if not product_model.get_product_by_id(id):
        return None

    nome = dados.get("nome", "")
    descricao = dados.get("descricao", "")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    categoria = dados.get("categoria", "geral")

    if not nome:
        raise ValueError("Nome é obrigatório")
    if preco is None or preco < 0:
        raise ValueError("Preço não pode ser negativo")
    if estoque is None or estoque < 0:
        raise ValueError("Estoque não pode ser negativo")

    product_model.update_product(id, nome, descricao, preco, estoque, categoria)
    return True


def delete_product(id):
    if not product_model.get_product_by_id(id):
        return None
    product_model.delete_product(id)
    return True


def search_products(termo, categoria=None, preco_min=None, preco_max=None):
    return product_model.search_products(termo, categoria, preco_min, preco_max)
