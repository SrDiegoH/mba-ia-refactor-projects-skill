from werkzeug.security import generate_password_hash
import models.user as user_model


def list_users():
    return user_model.get_all_users()


def get_user(id):
    return user_model.get_user_by_id(id)


def create_user(dados):
    nome = dados.get("nome", "")
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios")

    senha_hash = generate_password_hash(senha)
    return user_model.create_user(nome, email, senha_hash)
