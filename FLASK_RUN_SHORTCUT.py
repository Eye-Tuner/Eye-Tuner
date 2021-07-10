"""Shortcut for flask server."""

if __name__ == '__main__':
    from eyetuner_flask.app import create_app, run_kwargs
    create_app().run(**run_kwargs)
