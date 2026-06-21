from flask import request, jsonify
from services.report_service import ReportService

_service = ReportService()

NOT_FOUND_ERRORS = {'Usuário não encontrado', 'Categoria não encontrada'}

def _error_status(msg):
    if msg in NOT_FOUND_ERRORS:
        return 404
    return 400

def summary_report():
    data, error = _service.get_summary()
    if error:
        return jsonify({'error': error}), 500
    return jsonify(data), 200

def user_report(user_id):
    data, error = _service.get_user_report(user_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(data), 200

def get_categories():
    data, error = _service.get_categories()
    if error:
        return jsonify({'error': error}), 500
    return jsonify(data), 200

def create_category():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    result, error = _service.create_category(data)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(result), 201

def update_category(cat_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400
    result, error = _service.update_category(cat_id, data)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify(result), 200

def delete_category(cat_id):
    success, error = _service.delete_category(cat_id)
    if error:
        return jsonify({'error': error}), _error_status(error)
    return jsonify({'message': 'Categoria deletada'}), 200
