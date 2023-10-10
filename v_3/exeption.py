def get_trace() -> str:
    frame = inspect.currentframe().f_back.f_back
    return f'file: {frame.f_code.co_filename.split(os.sep)[-1]}, func: {frame.f_code.co_name}, line: {frame.f_lineno}'