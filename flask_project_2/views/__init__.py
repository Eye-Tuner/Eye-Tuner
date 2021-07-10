from .auth import bp as auth_bp
from .eyetracking import bp as eyetracking_bp
from .index import bp as index_bp


def register_all(app):
    for bp in (auth_bp, eyetracking_bp, index_bp, ):
        app.register_blueprint(bp)
    return app
