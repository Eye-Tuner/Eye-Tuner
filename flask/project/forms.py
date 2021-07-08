from models import Fcuser
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
# from wtforms.validators import Email
# from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    class UserID(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = field.data
            if Fcuser.query.filter_by(userid=userid).first():
                raise ValueError(f'id "{userid}" already exists!')

    userid = StringField('userid', validators=[DataRequired(), Length(min=-1, max=32), UserID()])
    username = StringField('username', validators=[DataRequired(), Length(max=8)])
    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('repassword', '비밀번호가 일치하지 않습니다')])
    repassword = PasswordField('repassword', validators=[DataRequired()])
    # email = EmailField('이메일', [DataRequired(), Email()])  # pip install email-validator


class LoginForm(FlaskForm):

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
        
        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            
            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if not fcuser:
                # Time Problem
                generate_password_hash('dummy password')
            elif check_password_hash(fcuser.password, password):
                return  # login success
            raise ValueError('User does not exist, or got wrong password!')  # login fail

    userid = StringField('userid', validators=[DataRequired(), Length(min=-1, max=30)])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])
