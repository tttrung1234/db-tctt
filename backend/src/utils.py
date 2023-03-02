def exception_handler(fn):
    def wrapprer(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except Exception as e:
            print(f'Error: {e}')
            print(f'At: {fn.__name__}')

    return wrapprer