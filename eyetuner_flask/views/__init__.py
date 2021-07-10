from .auth import bp as auth_bp
from .eyetracking import bp as eyetracking_bp
from .index import bp as index_bp


def init_app(app):
    from flask import Blueprint
    for bp in globals().values():
        if isinstance(bp, Blueprint):
            app.register_blueprint(bp)
    return app
