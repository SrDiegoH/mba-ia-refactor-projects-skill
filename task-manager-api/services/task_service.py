from database import db
from models.task import Task
from models.user import User
from models.category import Category
from sqlalchemy.orm import joinedload
from datetime import datetime
from utils.helpers import VALID_STATUSES, MIN_TITLE_LENGTH, MAX_TITLE_LENGTH, DEFAULT_PRIORITY

class TaskService:

    def get_all_tasks(self):
        tasks = Task.query.options(
            joinedload(Task.user),
            joinedload(Task.category)
        ).all()
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data['overdue'] = t.is_overdue()
            task_data['user_name'] = t.user.name if t.user else None
            task_data['category_name'] = t.category.name if t.category else None
            result.append(task_data)
        return result

    def get_task_by_id(self, task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return None, 'Task não encontrada'
        data = task.to_dict()
        data['overdue'] = task.is_overdue()
        return data, None

    def search_tasks(self, query='', status='', priority='', user_id=''):
        q = Task.query

        if query:
            q = q.filter(
                db.or_(
                    Task.title.like(f'%{query}%'),
                    Task.description.like(f'%{query}%')
                )
            )
        if status:
            q = q.filter(Task.status == status)
        if priority:
            q = q.filter(Task.priority == int(priority))
        if user_id:
            q = q.filter(Task.user_id == int(user_id))

        return [t.to_dict() for t in q.all()], None

    def get_stats(self):
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        overdue_count = sum(
            1 for t in Task.query.all() if t.is_overdue()
        )

        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }, None

    def create_task(self, data):
        title = data.get('title')
        if not title:
            return None, 'Título é obrigatório'
        if len(title) < MIN_TITLE_LENGTH:
            return None, 'Título muito curto'
        if len(title) > MAX_TITLE_LENGTH:
            return None, 'Título muito longo'

        status = data.get('status', 'pending')
        if status not in VALID_STATUSES:
            return None, 'Status inválido'

        priority = data.get('priority', DEFAULT_PRIORITY)
        if priority < 1 or priority > 5:
            return None, 'Prioridade deve ser entre 1 e 5'

        user_id = data.get('user_id')
        if user_id and not db.session.get(User, user_id):
            return None, 'Usuário não encontrado'

        category_id = data.get('category_id')
        if category_id and not db.session.get(Category, category_id):
            return None, 'Categoria não encontrada'

        task = Task()
        task.title = title
        task.description = data.get('description', '')
        task.status = status
        task.priority = priority
        task.user_id = user_id
        task.category_id = category_id

        due_date = data.get('due_date')
        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                return None, 'Formato de data inválido. Use YYYY-MM-DD'

        tags = data.get('tags')
        if tags:
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        try:
            db.session.add(task)
            db.session.commit()
            return task.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, 'Erro ao criar task'

    def update_task(self, task_id, data):
        task = db.session.get(Task, task_id)
        if not task:
            return None, 'Task não encontrada'

        if 'title' in data:
            if len(data['title']) < MIN_TITLE_LENGTH:
                return None, 'Título muito curto'
            if len(data['title']) > MAX_TITLE_LENGTH:
                return None, 'Título muito longo'
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in VALID_STATUSES:
                return None, 'Status inválido'
            task.status = data['status']

        if 'priority' in data:
            if data['priority'] < 1 or data['priority'] > 5:
                return None, 'Prioridade deve ser entre 1 e 5'
            task.priority = data['priority']

        if 'user_id' in data:
            if data['user_id'] and not db.session.get(User, data['user_id']):
                return None, 'Usuário não encontrado'
            task.user_id = data['user_id']

        if 'category_id' in data:
            if data['category_id'] and not db.session.get(Category, data['category_id']):
                return None, 'Categoria não encontrada'
            task.category_id = data['category_id']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError:
                    return None, 'Formato de data inválido'
            else:
                task.due_date = None

        if 'tags' in data:
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']

        task.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return task.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, 'Erro ao atualizar'

    def delete_task(self, task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return False, 'Task não encontrada'

        try:
            db.session.delete(task)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, 'Erro ao deletar'
