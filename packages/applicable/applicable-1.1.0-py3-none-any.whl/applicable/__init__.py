"""Package for testing if callables can be called with specified arguments
without raising an exception, with the applicable() function."""

__author__ = 'Finn Mason'
__version__ = '1.1.0'
__all__ = [
    '_FalseException',
    'applicable'
]

from typing import Any, Callable

class _FalseException(Exception):
                """Exception returned by applicable()
                
                Overrides the bool method; use cls attribute to determine type of exception
                """
                def __init__(self, exc_inst):
                    super().__init__()
                    self.inst = exc_inst
                    self.cls = exc_inst.__class__
                    
                def __bool__(self):
                    return False
                
                def __eq__(self, other):
                    return isinstance(other, self.__class__)
                
                def __repr__(self):
                    return f'{__name__}._FalseException(exc_inst={self.cls.__name__}(...))'

def applicable(callable: Callable, *args: Any, **kwargs: Any) -> Any:
    """Tests if callables can be called with specified arguments without raising an exception.
    
    
    There are two special keyword arguments: ret_exc and ret_result.
    
    ret_exc: Type or value to return upon error. Defaults to _FalseException. With 
    the exception of _FalseException (which is returned as _FalseException
    (exception_instance)), the default value for the type is returned, e.g.,
    int() (which is 0), bool() (False), None, if ret_exc is a type. If ret_exc
    is a value, the value is returned.
    ret_result: Whether to return the result of the operation upon no error.
    Defaults to True.
    
    Other keyword arguments are passed to the callable.
    """

    ret_result = kwargs.get('ret_result', True)
    ret_exc = kwargs.get('ret_exc', _FalseException)
    if 'ret_exc' in kwargs: del kwargs['ret_exc']
    if 'ret_result' in kwargs: del kwargs['ret_result']
    
    try:
        ret = callable(*args, **kwargs)
    except Exception as exc:
        if ret_exc is _FalseException:
            return _FalseException(exc)
        elif ret_exc == None:
            return
        elif isinstance(ret_exc, type):
            return ret_exc()
        else:
            return ret_exc
    else:
        if ret_result:
            return ret
        return True

if __name__ == '__main__':
    a = applicable(int, '42')
    b = applicable(int, 'yee')