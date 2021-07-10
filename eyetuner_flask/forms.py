from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
# from wtforms.validators import Email
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired(), Length(min=8, max=32)])
    username = StringField('username', validators=[DataRequired(), Length(max=16)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    repassword = PasswordField('repassword', validators=[
        DataRequired(), EqualTo('repassword', '비밀번호가 일치하지 않습니다')])
    email = EmailField('이메일', [
        DataRequired(),
        # Email()  # pip install email-validator
    ])


class LoginForm(FlaskForm):

    # 이 기능을 view 로 이동했습니다.
    # class UserPassword(object):
    #     def __init__(self, message=None):
    #         self.message = message
    #
    #     def __call__(self, form, field):
    #         userid = form['userid'].data
    #         password = field.data
    #
    #         fcuser = Fcuser.query.filter_by(userid=userid).first()
    #         if not fcuser:
    #             # Time Problem
    #             generate_password_hash('dummy password')
    #         elif check_password_hash(fcuser.password, password):
    #             return  # login success
    #         raise ValueError('User does not exist, or got wrong password!')

    userid = StringField('userid', validators=[DataRequired(), Length(min=8, max=32)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
