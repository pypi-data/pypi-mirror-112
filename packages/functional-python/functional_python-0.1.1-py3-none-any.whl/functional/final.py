from dataclasses import dataclass

from .typing_wrapper import *

C = TypeVar('C')

@dataclass(frozen=True)
class FinalInheritanceError(TypeError, Generic[C]):
    """ An exception that is thrown whenever final class is to be inherited from """
    
    cls: Type[C]
    """ A final class being inherited from """
    
    def __post_init__(self):
        super().__init__(Exception(self.message))
    
    @property
    def message(self) -> str:
        """ String representation of the error message """
        return f"Cannot inherit from final class {repr(self.cls.__qualname__)}."

def __init_subclass_exception__(cls, **kwargs):
    raise FinalInheritanceError(cls)

def final_class(cls: Type[C]) -> Type[C]:
    """
    A Decoration which makes the given class `cls` final.
    When inherited, the `FinalInheritanceError` will be raised.
    Also wraps it with `typing.final` decoration if exists, but some IDEs ignore it.
    
    Args:
        cls: A class to be made final.

    Returns:
        Returns the same class.
    """
    
    setattr(cls, '__init_subclass_exception__', classmethod(__init_subclass_exception__))
    cls.__init_subclass__ = cls.__init_subclass_exception__
    return final(cls)


__all__ = \
[
    # Own implementations
    'FinalInheritanceError',
    'final_class',
]
