from .auth import bp as auth_bp
from .eyetracking import bp as eyetracking_bp


def register_all(app):
    for bp in (auth_bp, eyetracking_bp, ):
        app.register_blueprint(bp)
    return app
