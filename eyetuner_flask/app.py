from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Directory Patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
del sys, os
# Directory Patch End

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

del SQLAlchemy, Migrate, CSRFProtect


def create_app():

    # Initialize
    from flask import Flask
    app = Flask(__name__)

    # Config
    import eyetuner_flask.config as conf
    app.config.from_object(conf)

    # CSRF
    csrf.init_app(app)

    # ORM
    db.init_app(app)
    # db.app = app
    # db.create_all()
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    import eyetuner_flask.models  # NOQA

    # Blueprints
    import eyetuner_flask.views as v
    v.init_app(app)

    # Filters
    import eyetuner_flask.filters as f
    # _ = {app.template_filter(v) for k, v in f.__dict__.items() if k in f.__all__}
    app.jinja_env.filters.update({k: v for k, v in f.__dict__.items() if k in f.__all__})

    # Context Processors
    import eyetuner_flask.context_processors as c
    _ = {app.context_processor(v) for k, v in c.__dict__.items() if k in c.__all__}

    # Session Handler
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=10)
    from flask import session
    import datetime
    app.before_request(make_session_permanent)

    return app


run_kwargs = dict(
    host='127.0.0.1',
    port=5000,
    debug=True
)

# # HTTPS Settings
# import ssl
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='secret')
# run_kwargs.update(ssl_context=ssl_context)


if __name__ == "__main__":
    create_app().run(**run_kwargs)
