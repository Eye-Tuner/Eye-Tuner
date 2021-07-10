"""Context Processors used by all views."""
from flask import g

__all__ = ['fetch_user', 'register_datetime_func']


def fetch_user():
    return dict(user=g.user)


def register_datetime_func():  # usage: {{ datetime(value) }}
    def datetime(value, fmt="%Y년 %m월 %d일 %H:%M"):
        return value.strftime(fmt)
    return dict(datetime=datetime)
