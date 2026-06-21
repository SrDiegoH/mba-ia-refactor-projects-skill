from werkzeug.security import check_password_hash
import models.user as user_model


def login(email, senha):
    if not email or not senha:
        raise ValueError("Email e senha são obrigatórios")

    usuario = user_model.get_user_by_email(email)
    if not usuario:
        return None

    if not check_password_hash(usuario["senha"], senha):
        return None

    return {
        "id": usuario["id"],
        "nome": usuario["nome"],
        "email": usuario["email"],
        "tipo": usuario["tipo"]
    }
