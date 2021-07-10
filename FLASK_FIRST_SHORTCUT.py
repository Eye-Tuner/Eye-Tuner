"""Run this script when first running flask server"""

if __name__ == '__main__':
    import os
    import flask_migrate
    from eyetuner_flask.app import create_app
    os.chdir('eyetuner_flask')
    app = create_app()
    with app.app_context():
        flask_migrate.upgrade()
