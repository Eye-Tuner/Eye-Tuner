from flask import Blueprint, render_template

bp = Blueprint('eyetracking', __name__, url_prefix='/dev')


@bp.route('/ex0/')
def wink_scroll_example():
    return render_template('eyetracking/ex0_wink_scroll.html')


@bp.route('/ex1/')
def webgazer_example():
    return render_template('eyetracking/ex1_empty_page.html')


@bp.route('/eye_tuner_detector_web/')
def eye_tuner_detector_web():
    return render_template('eyetracking/eye_tuner_detector_web.html')
