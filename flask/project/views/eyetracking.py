from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect

bp = Blueprint('eyetracking', __name__, url_prefix='/dev')


@bp.route('/ex0/')
def wink_scroll_example():
    return render_template('eyetracking/ex0_wink_scroll.html')


@bp.route('/ex1/')
def webgazer_example():
    return render_template('eyetracking/ex1_empty_page.html')


@bp.route('/blink_counter/')
def blink_counter():
    return render_template('eyetracking/blink_counter.html')
