from database import db
from models.user import User
from models.task import Task
from utils.helpers import validate_email, VALID_ROLES, MIN_PASSWORD_LENGTH

class UserService:

    def get_all_users(self):
        users = User.query.all()
        result = []
        for u in users:
            user_data = u.to_dict()
            user_data['task_count'] = len(u.tasks)
            result.append(user_data)
        return result

    def get_user_by_id(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return None, 'Usuário não encontrado'
        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in Task.query.filter_by(user_id=user_id).all()]
        return data, None

    def get_user_tasks(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return None, 'Usuário não encontrado'
        tasks = Task.query.filter_by(user_id=user_id).all()
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data['overdue'] = t.is_overdue()
            result.append(task_data)
        return result, None

    def create_user(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            return None, 'Nome é obrigatório'
        if not email:
            return None, 'Email é obrigatório'
        if not password:
            return None, 'Senha é obrigatória'

        if not validate_email(email):
            return None, 'Email inválido'

        if len(password) < MIN_PASSWORD_LENGTH:
            return None, f'Senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres'

        if role not in VALID_ROLES:
            return None, 'Role inválido'

        if User.query.filter_by(email=email).first():
            return None, 'Email já cadastrado'

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        try:
            db.session.add(user)
            db.session.commit()
            return user.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, 'Erro ao criar usuário'

    def update_user(self, user_id, data):
        user = db.session.get(User, user_id)
        if not user:
            return None, 'Usuário não encontrado'

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not validate_email(data['email']):
                return None, 'Email inválido'
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return None, 'Email já cadastrado'
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < MIN_PASSWORD_LENGTH:
                return None, 'Senha muito curta'
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in VALID_ROLES:
                return None, 'Role inválido'
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        try:
            db.session.commit()
            return user.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, 'Erro ao atualizar'

    def delete_user(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return False, 'Usuário não encontrado'

        try:
            Task.query.filter_by(user_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, 'Erro ao deletar'

    def authenticate(self, email, password):
        if not email or not password:
            return None, 'Email e senha são obrigatórios'

        user = User.query.filter_by(email=email).first()
        if not user:
            return None, 'Credenciais inválidas'

        if not user.check_password(password):
            return None, 'Credenciais inválidas'

        if not user.active:
            return None, 'Usuário inativo'

        return user, None
