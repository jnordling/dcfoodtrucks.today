from datetime import datetime
from flask import request, session
from . import main
from ..models import User


def is_home_page():
    return True if request.path == '/' else False


def get_current_user():
    user = None
    if 'logged_in' in session:
        try:
            user = User.query.get(int(session['user']['id']))
        except:
            pass
    return user


@main.context_processor
def helper_vars():
    return dict(
        is_home_page=is_home_page(),
    )
