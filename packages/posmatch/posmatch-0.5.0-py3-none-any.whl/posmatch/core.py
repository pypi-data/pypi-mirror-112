"""
Enable positional sub-pattern matching for objects of a custom class by
setting the `__match_args__` class attribute.

This module provides the following functions and classes:

  pos_match       -    class decorator setting the `__match_args__`
                       attribute
  PosMatchMeta    -    metaclass setting the `__match_args__` attribute
  PosMatchMixin   -    mix-in class setting the `__match_args__`
                       attribute
"""

import inspect


def pos_match(cls=None, /, *, force=False):
    """Decorator setting the `__match_args__` class attribute.

    `__match_args__` will contain a sequence of names equal to
    parameter names in the signature of `cls.__init__` (not including
    `self`).

    If `cls` already has the `__match_args__` attribute (inherited or
    defined on its own) it will not be set, unless `force` is set to
    True.
    """
    if cls:
        # @pos_match usage
        if not hasattr(cls, '__match_args__'):
            _set_match_args(cls)
        return cls

    if force:
        # @pos_match(force=True) or equivalent usage
        return _set_match_args

    # @pos_match(), @pos_match(force=False) or equivalent usage
    return pos_match


def _set_match_args(cls):
    cls.__match_args__ = _param_names_from_init(cls)

    # also return the class so this function can be used as a decorator
    return cls


def _param_names_from_init(cls):
    init_params = inspect.signature(cls.__init__).parameters

    # exclude the first parameter (self)
    return tuple(init_params)[1:]


class PosMatchMeta(type):
    """Metaclass setting the `__match_args__` class attribute."""

    def __new__(mcs, *args):
        cls = super().__new__(mcs, *args)
        if not hasattr(cls, '__match_args__'):
            _set_match_args(cls)
        return cls


class PosMatchMixin:
    """Mix-in class setting the `__match_args__` class attribute."""

    @classmethod
    @property
    def __match_args__(cls):
        return _param_names_from_init(cls)
