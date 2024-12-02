from functools import wraps
from flask import abort, render_template
from flask_login import current_user

def permission_required(index):
    """指定された権限が必要な閲覧を保護するデコレータ"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(index):
                return render_template('no_permission.html')
            return func(*args, **kwargs)
        return wrapper
    return decorator