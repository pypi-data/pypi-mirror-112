"""Package for testing if callables can be called with specified arguments
without raising an exception, with the applicable() function."""

__author__ = 'Finn Mason'
__version__ = '1.0.1'
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
    
    ret_exc: Whether to return the exception raised upon error (in the form
    of a _FalseException). Defaults to True.
    ret_result: Whether to return the result of the operation upon no error.
    Defaults to True.
    
    Other keyword arguments are passed to the callable.
    """

    ret_result = kwargs.get('ret_result', True)
    ret_exc = kwargs.get('ret_exc', True)
    if 'ret_exc' in kwargs: del kwargs['ret_exc']
    if 'ret_result' in kwargs: del kwargs['ret_result']
    
    try:
        ret = callable(*args, **kwargs)
    except Exception as e:
        if ret_exc:
            return _FalseException(e)
        return False
    else:
        if ret_result:
            return ret
        return True

if __name__ == '__main__':
    a = applicable(int, '42')
    b = applicable(int, 'yee')