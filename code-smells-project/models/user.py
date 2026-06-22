from config.database import get_db
from utils.db_utils import row_to_dict

_USER_FIELDS = ["id", "nome", "email", "tipo", "criado_em"]


def _row_to_dict(row, include_senha=False):
    data = row_to_dict(row, _USER_FIELDS)
    if include_senha:
        data["senha"] = row["senha"]
    return data


def get_all_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [_row_to_dict(row) for row in cursor.fetchall()]


def get_user_by_id(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    row = cursor.fetchone()
    return _row_to_dict(row) if row else None


def get_user_by_email(email):
    """Retorna usuário com hash de senha — usado apenas para autenticação."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    return _row_to_dict(row, include_senha=True) if row else None


def create_user(nome, email, senha_hash, tipo="cliente"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, senha_hash, tipo)
    )
    db.commit()
    return cursor.lastrowid
