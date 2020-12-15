from pprint import pprint


def foo():
    print(f'function {foo.__name__} is called')


# pprint(foo.__dir__())  # we look there method __call__ thanks which our function is callable.
#  Exactly __call__ distinguishes functions from other methods
# _________________________________________________________________________

# You also can add functions in list and iter with them
x = foo
n = foo
y = foo
lst = [x, n, y, foo]

# for i in lst:
#     i.__call__()  # the same that i()
# _________________________________________________________________________

# You can put one function into other
from typing import Callable


def foo2(function: Callable):
    print(f'function {foo2.__name__} is called')
    function()


# foo2(foo)
# _________________________________________________________________________

# Let's try create function via class
class MyFunction:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        print('The exemplar of class MyFunction is called')


my_exemplar = MyFunction()


# my_exemplar.__call__()  # the same that my_exemplar()
# _________________________________________________________________________

def multiplier(a, b):
    return a * b


def print_fabric(old_function: Callable):
    def new_function(a, b):
        print(f'Вызвана функция {old_function.__name__}')
        print(f'С аргументами {a, b}')
        result = old_function(a, b)
        print(f'Получили результат {result}')
        return result

    return new_function


multiplier = print_fabric(multiplier)  # Now there is a new functional in multiplier


# multiplier.__call__(2, 3)
# _________________________________________________________________________
@print_fabric
def multiplier2(a, b):
    return a * b


# multiplier.__call__(2, 3)

# _________________________________________________________________________
def print_decor(old_function: Callable): ...


def my_foo(*args, **kwargs):
    print(args)
    print(kwargs)


# my_foo(1, 2, 3, a=4, b=5)  # unnamed args will go to tuple (1, 2, 3), named arguments will go dict {'a': 4, 'b': 5}


# _________________________________________________________________________
# let's try unpack tuple & dict on other example
def foo_(a, b, c, d, e):
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)


tuple_ = 1, 2, 3
dict_ = {
    'd': 4,
    'e': 5
}


# foo_(*tuple_, **dict_)


# _________________________________________________________________________


def _fabric(old_function):
    def new_function(*args, **kwargs):
        print(f'Вызвана функция {old_function.__name__}')
        print(f'С аргументами {args, kwargs}')
        result = old_function(*args, **kwargs)
        print(f'Получили результат {result}')
        return result

    return new_function


@_fabric
def multiplier3(a, b):
    return a * b


# multiplier3.__call__(1, 2)
# _________________________________________________________________________

# let's engage our decorator in <try> constructions
TRIES = 10


def attempted_decorator(any_function: Callable):
    def new_function(*args, **kwargs):
        my_error = None  # we had to use combination <my_error = None> to avoid this error:
        # variable <my_exception> mae be referenced before assignment
        for i in range(TRIES):
            try:
                return any_function(*args, **kwargs)
            except Exception as my_exception:
                my_error = my_exception
                print(f'The number of trying №{i}')
                print(my_exception)
        raise my_error

    return new_function


@attempted_decorator
def multiplier4(a, b):
    return a / b


# x = multiplier4(2, 0)
# print(x)
# _________________________________________________________________________
# let's try append my_error into list payload_errors
TRIES2 = 10


def send_errors(errors):
    print(errors)


def attempted_decorator2(any_function2: Callable):
    payload_errors = []
    max_errors = 3

    def new_function2(*args, **kwargs):
        nonlocal payload_errors
        my_error = None  # we had to use combination <my_error = None> to avoid this error:
        # variable <my_exception> mae be referenced before assignment
        for i in range(TRIES2):
            try:
                return any_function2(*args, **kwargs)
            except Exception as my_exception:
                my_error = my_exception
                print(f'The number of trying №{i}')
                print(my_exception)
        payload_errors.append(my_error)
        if len(payload_errors) == max_errors:
            send_errors(payload_errors)
            payload_errors = []  # zero out

    return new_function2


@attempted_decorator2
def multiplier5(a, b):
    return a / b


# x = multiplier5(2, 0)
# x = multiplier5(2, 0)
# x = multiplier5(2, 0)
# print(x)
# _________________________________________________________________________
# now let's write a decorator which receive arguments
def send_errors_(errors):
    print(errors)


def fabric_trouble_decorator(n_tries, errors, callback=None):
    def trouble_decorator(old_function: Callable):
        payload_errors = []
        max_errors = 3

        def new_function(*args, **kwargs):
            nonlocal payload_errors
            error = None
            for i in range(n_tries):
                try:
                    return old_function(*args, **kwargs)
                except errors as er:
                    error = er
                    if callback:
                        callback()
                    print(er)
            payload_errors.append(error)
            if len(payload_errors) == max_errors:
                send_errors_(payload_errors)
                payload_errors = []

        return new_function

    return trouble_decorator


@fabric_trouble_decorator(15, ZeroDivisionError)
def multiplier_(a, b):
    return a / b


# x = multiplier_(1, 8)
# y = multiplier_(1, 0)
# print(y)
# print(x)
# _________________________________________________________________________
# 2 decorators from teacher

import datetime
import logging
from logging.handlers import RotatingFileHandler
from typing import Callable, Any


def make_trace(path: str) -> Callable:
    """Вариант с записью в файл"""

    def trace(old_function: Callable) -> Callable:
        def new_function(*args, **kwargs) -> Any:
            result = old_function(*args, **kwargs)

            with open(path, 'a') as log:
                log.write(f'\n{datetime.datetime.utcnow()}: called {old_function.__name__}\n'
                          f'\t args: {args}\n'
                          f'\t kwargs: {kwargs}\n'
                          f'\t result: {result}\n')

            return result

        return new_function

    return trace


def make_log(path: str) -> Callable:
    """Вариант с использованием logging"""

    def log(old_function: Callable) -> Callable:
        logger = logging.getLogger(path)
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(path, backupCount=10, maxBytes=1000000)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        def new_function(*args, **kwargs) -> Any:
            result = old_function(*args, **kwargs)

            logger.info(f'called: {old_function.__name__}\n'
                        f'\t args: {args}\n'
                        f'\t kwargs: {kwargs}\n'
                        f'\t result: {result}\n')
            return result

        return new_function

    return log
