from flask import request, jsonify
from services.user_service import UserService

_service = UserService()

NOT_FOUND_ERRORS = {'Usuário não encontrado'}
CONFLICT_ERRORS = {'Email já cadastrado'}

def _error_status(msg):
    if msg in NOT_FOUND_ERRORS:
        return 404
    if msg in CONFLICT_ERRORS:
        return 409
    if msg in {'Usuário inativo'}:
        return 403
    if msg in {'Credenciais inválidas'}:
        return 401
    return 400

def get_users():
    return jsonify(_service.get_all_users()), 200

def get_user(user_id):
    data, error = _service.get_user_by_id(user_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(data), 200

def get_user_tasks(user_id):
    data, error = _service.get_user_tasks(user_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(data), 200

def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    result, error = _service.create_user(data)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(result), 201

def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    result, error = _service.update_user(user_id, data)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(result), 200

def delete_user(user_id):
    success, error = _service.delete_user(user_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200

def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    user, error = _service.authenticate(data.get('email'), data.get('password'))
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify({
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'token': 'fake-jwt-token-' + str(user.id)
    }), 200
