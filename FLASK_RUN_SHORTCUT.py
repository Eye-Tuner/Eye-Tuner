"""Shortcut for flask server."""

if __name__ == '__main__':
    from eyetuner_flask.app import create_app, default_options
    create_app().run(**default_options)
