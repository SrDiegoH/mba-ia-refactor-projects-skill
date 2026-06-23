import re

def calculate_percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)

def validate_email(email):
    if re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
        return True
    return False

def is_valid_color(color):
    if color and len(color) == 7 and color[0] == '#':
        return True
    return False

VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']
VALID_ROLES = ['user', 'admin', 'manager']
MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MIN_PASSWORD_LENGTH = 4
DEFAULT_PRIORITY = 3
