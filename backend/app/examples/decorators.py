def print_args(function):
    def wrapper(*args, **kwargs):
        print('Arguments:', args, kwargs)
        return function(*args, **kwargs)
    return wrapper


@print_args
def write(text):
    print(text)


write('foo')
