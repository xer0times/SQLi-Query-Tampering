## Burp Exceptions Fix magic code
import sys, functools, inspect, traceback

def decorate_function(original_function):
    @functools.wraps(original_function)
    def decorated_function(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
        except:
            sys.stdout.write('\n\n*** PYTHON EXCEPTION\n')
            traceback.print_exc(file=sys.stdout)
            raise
    return decorated_function

def FixBurpExceptionsForClass(cls):
    for name, method in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls, name, decorate_function(method))        
    return cls

def FixBurpExceptions():
    for name, cls in inspect.getmembers(sys.modules['__main__'], predicate=inspect.isclass):
        FixBurpExceptionsForClass(cls)

        
