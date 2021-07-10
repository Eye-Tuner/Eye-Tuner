from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from forms import LoginForm, RegisterForm
from models import Fcuser, db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/logout/', methods=('GET', ))
def logout():
    session.pop('userid', None)
    return redirect('/')


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = Fcuser.query.filter_by(userid=form.userid.data).first().id
        return redirect('/')
    return render_template('auth/login.html', form=form)


@bp.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():

        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = generate_password_hash(form.data.get('password'))

        db.session.add(fcuser)
        db.session.commit()
        print('register success')

        return redirect('/')

    return render_template('auth/register.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    id = session.get('userid')
    if id is None:
        g.user = None
    else:
        g.user = Fcuser.query.get(id)


@bp.context_processor
def fetch_user():
    return dict(user=g.user)


@bp.context_processor
def make_simple_func():
    def datetime(value, fmt="%Y년 %m월 %d일 %H:%M"):
        return value.strftime(fmt)
    return dict(datetime=datetime)


# @bp.route('/signup/', methods=('GET', 'POST'))
# def signup():
#     form = UserRegisterForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if not user:
#             user = User(
#                 username=form.username.data,
#                 password=generate_password_hash(form.password.data),
#             )
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('main.index'))
#         else:
#             flash('이미 존재하는 사용자입니다.')
#     return render_template('login.html', form=form)
#
#
# @bp.route('/login/', methods=('GET', 'POST'))
# def login():
#     form = UserLoginForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if not user:
#             generate_password_hash('')
#             flash("존재하지 않는 사용자입니다.")
#         elif not check_password_hash(user.password, form.password.data):
#             flash("비밀번호가 올바르지 않습니다.")
#         else:
#             session.clear()
#             session['user_id'] = user.id
#             # next_url = request.args.get('next', type=str, default=None)
#             # if next_url:
#             #     return redirect(next_url)
#             return redirect(url_for('main.index'))
#     return render_template('auth/login.html', form=form)
#
#
