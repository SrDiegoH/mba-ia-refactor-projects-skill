from flask import request, jsonify
from services.task_service import TaskService

_service = TaskService()

NOT_FOUND_ERRORS = {'Task não encontrada', 'Usuário não encontrado', 'Categoria não encontrada'}

def _error_status(msg):
    if msg in NOT_FOUND_ERRORS:
        return 404
    return 400

def get_tasks():
    return jsonify(_service.get_all_tasks()), 200

def get_task(task_id):
    data, error = _service.get_task_by_id(task_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(data), 200

def search_tasks():
    data, error = _service.search_tasks(
        query=request.args.get('q', ''),
        status=request.args.get('status', ''),
        priority=request.args.get('priority', ''),
        user_id=request.args.get('user_id', '')
    )
    if error:
        return jsonify({'error': error}), 400
    return jsonify(data), 200

def task_stats():
    data, error = _service.get_stats()
    if error:
        return jsonify({'error': error}), 500
    return jsonify(data), 200

def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    result, error = _service.create_task(data)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(result), 201

def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    result, error = _service.update_task(task_id, data)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(result), 200

def delete_task(task_id):
    success, error = _service.delete_task(task_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify({'message': 'Task deletada com sucesso'}), 200
