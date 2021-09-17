from . import auth
from . import eyetracking
from . import index

from .auth import bp as auth_bp
from .eyetracking import bp as eyetracking_bp
from .index import bp as index_bp


def init_app(app):
    from flask import Blueprint
    for name, bp in globals().items():
        if not name.startswith('_') and isinstance(bp, Blueprint):
            app.register_blueprint(bp)
    return app
