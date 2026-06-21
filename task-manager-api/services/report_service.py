from database import db
from models.task import Task
from models.user import User
from models.category import Category
from datetime import datetime, timedelta
from utils.helpers import calculate_percentage

class ReportService:

    def get_summary(self):
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()

        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        overdue_list = []
        for t in Task.query.all():
            if t.is_overdue():
                overdue_list.append({
                    'id': t.id,
                    'title': t.title,
                    'due_date': str(t.due_date),
                    'days_overdue': (datetime.utcnow() - t.due_date).days
                })

        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
        recent_done = Task.query.filter(
            Task.status == 'done',
            Task.updated_at >= seven_days_ago
        ).count()

        user_stats = []
        for u in User.query.all():
            user_tasks = Task.query.filter_by(user_id=u.id).all()
            total = len(user_tasks)
            completed = sum(1 for t in user_tasks if t.status == 'done')
            user_stats.append({
                'user_id': u.id,
                'user_name': u.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': calculate_percentage(completed, total)
            })

        return {
            'generated_at': str(datetime.utcnow()),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': {
                'pending': pending,
                'in_progress': in_progress,
                'done': done,
                'cancelled': cancelled,
            },
            'tasks_by_priority': {
                'critical': Task.query.filter_by(priority=1).count(),
                'high': Task.query.filter_by(priority=2).count(),
                'medium': Task.query.filter_by(priority=3).count(),
                'low': Task.query.filter_by(priority=4).count(),
                'minimal': Task.query.filter_by(priority=5).count(),
            },
            'overdue': {
                'count': len(overdue_list),
                'tasks': overdue_list,
            },
            'recent_activity': {
                'tasks_created_last_7_days': recent_tasks,
                'tasks_completed_last_7_days': recent_done,
            },
            'user_productivity': user_stats,
        }, None

    def get_user_report(self, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return None, 'Usuário não encontrado'

        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        done = pending = in_progress = cancelled = overdue = high_priority = 0

        for t in tasks:
            if t.status == 'done':
                done += 1
            elif t.status == 'pending':
                pending += 1
            elif t.status == 'in_progress':
                in_progress += 1
            elif t.status == 'cancelled':
                cancelled += 1

            if t.priority <= 2:
                high_priority += 1

            if t.is_overdue():
                overdue += 1

        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'statistics': {
                'total_tasks': total,
                'done': done,
                'pending': pending,
                'in_progress': in_progress,
                'cancelled': cancelled,
                'overdue': overdue,
                'high_priority': high_priority,
                'completion_rate': calculate_percentage(done, total)
            }
        }, None

    def get_categories(self):
        categories = Category.query.all()
        result = []
        for c in categories:
            cat_data = c.to_dict()
            cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
            result.append(cat_data)
        return result, None

    def create_category(self, data):
        name = data.get('name')
        if not name:
            return None, 'Nome é obrigatório'

        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')

        try:
            db.session.add(category)
            db.session.commit()
            return category.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, 'Erro ao criar categoria'

    def update_category(self, cat_id, data):
        cat = db.session.get(Category, cat_id)
        if not cat:
            return None, 'Categoria não encontrada'

        if 'name' in data:
            cat.name = data['name']
        if 'description' in data:
            cat.description = data['description']
        if 'color' in data:
            cat.color = data['color']

        try:
            db.session.commit()
            return cat.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, 'Erro ao atualizar'

    def delete_category(self, cat_id):
        cat = db.session.get(Category, cat_id)
        if not cat:
            return False, 'Categoria não encontrada'

        try:
            db.session.delete(cat)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, 'Erro ao deletar'
