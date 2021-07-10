__all__ = ['datetime']


def datetime(value, fmt="%Y년 %m월 %d일 %H:%M"):  # usage: {{ value|datetime }}
    return value.strftime(fmt)
