from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from eyetuner_flask.forms import LoginForm, RegisterForm
from eyetuner_flask.models import Fcuser, db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# UTILS

USER_SESSION_KEY = 'user_id'


def _login_user(user):
    session.clear()
    session[USER_SESSION_KEY] = user.id


def _logout_user():
    session.pop(USER_SESSION_KEY, None)


def _get_user():
    return session.get(USER_SESSION_KEY, None)


@bp.before_app_request
def load_logged_in_user():
    user_id = _get_user()
    if user_id is None:
        g.user = None
    else:
        g.user = Fcuser.query.get(user_id)


# VIEWS

@bp.route('/logout/', methods=('GET', ))
def logout():
    _logout_user()
    return redirect('/')


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if _get_user() is not None:
        flash('이미 로그인되어 있습니다. 새로운 유저로 로그인하게 됩니다. ')
    if request.method == 'POST' and form.validate_on_submit():
        user = Fcuser.query.filter_by(userid=form.userid.data).first()
        if not user:  # Login fail
            generate_password_hash('')  # intended to wait time similar with checking password
            flash("존재하지 않는 사용자입니다.")
        elif not check_password_hash(user.password, form.password.data):  # Login fail
            flash("비밀번호가 올바르지 않습니다.")
        else:  # Login success
            _login_user(user)
            # next_url = request.args.get('next', type=str, default=None)
            # if next_url:
            #     return redirect(next_url)
            return redirect(url_for('index.index'))
        # # 실제 production 환경에서는 이 두 경우의 오류를 하나로 취급합니다.
        # flash('사용자가 존재하지 않거나, 비밀번호가 올바르지 않습니다.')
    return render_template('auth/login.html', form=form)


@bp.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Fcuser.query.filter_by(userid=form.userid.data).first()
        if not user:
            user = Fcuser(
                userid=form.userid.data,
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                email=form.email.data
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
        return redirect('/')
    return render_template('auth/register.html', form=form)
