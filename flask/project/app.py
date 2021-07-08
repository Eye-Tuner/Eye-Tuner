import os
import datetime
from flask import Flask, session

from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
# migrate = Migrate()  # todo: use migration
csrf = CSRFProtect()


def create_app():

    # Initialize
    app = Flask(__name__)

    # Config
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'ajserwhfdhkaudfhwkjeehw'

    # CSRF
    csrf.init_app(app)

    # ORM
    db.init_app(app)
    db.app = app
    db.create_all()
    # if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
    #     migrate.init_app(app, db, render_as_batch=True)
    # else:
    #     migrate.init_app(app, db)
    import models  # NOQA

    # Blueprints
    from views import register_all
    register_all(app)

    # Filters
    import filters
    app.jinja_env.filters.update({k: v for k, v in filters.__dict__.items() if not k.startswith('_')})

    # Session Handler
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=10)

    return app


if __name__ == "__main__":

    run_kwargs = dict(
        host='127.0.0.1',
        port=5000,
        debug=True
    )

    # # for HTTPS
    # import ssl
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='secret')
    # run_kwargs.update(ssl_context=ssl_context)

    create_app().run(**run_kwargs)
