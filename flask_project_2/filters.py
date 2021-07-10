def datetime(value, fmt="%Y년 %m월 %d일 %H:%M"):  # usage: {{ sample_data|datetime }}
    return value.strftime(fmt)
