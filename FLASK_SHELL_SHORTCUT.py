"""Shortcut for flask interactive shell."""

# Example:
# >>> from eyetuner_flask.models import Fcuser
# >>> Fcuser
# <class 'eyetuner_flask.models.Fcuser'>
# >>> Fcuser.query.all()
# []

if __name__ == '__main__':
    import code
    import sys
    from flask.cli import ScriptInfo
    from eyetuner_flask.app import create_app
    globals().update(ScriptInfo(create_app=create_app).load_app().make_shell_context())
    app = globals().get('app')
    app.app_context().push()
    code.interact(
        banner="Python %s on %s\nApp: %s [%s]\nInstance: %s"
               % (sys.version, sys.platform, app.import_name, app.env, app.instance_path),
        local=globals()
    )
