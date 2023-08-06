"""This is not module that configure library mypythontools, but module that help create config for your project.

What
====

1) Simple and short syntax.
2) Ability to have docstrings on variables (not dynamically, so visible in IDE).
3) Type checking, one-of-options checking.
4) Also function evaluation from other config values (not only static value stored)
5) Options hierarchy (nested options).

How
===

Boosted property with simplified implementation. To be able to provide docstrings in IDE, first function is created.

Examples:
=========

>>> class SimpleConfig(ConfigBase):
...    @myproperty(int)  # Use tuple like (str, int, bool) if more classes.
...    def var() -> int:  # This is for type hints in IDE.
...        '''This is docstrings (also visible in IDE, because not defined dynamically).'''
...        return 123  # This is initial value that can be edited.
...
...    @myproperty  # Brackets are not necessary
...    def evaluated(self) -> int:
...        return self.var + 1
...
>>> config = SimpleConfig()
>>> config.var
123
>>> config.var = 665
>>> config.var
665
>>> config.evaluated
666
>>> config.var = "String is problem"
Traceback (most recent call last):
TypeError: ...

You can also use options checker. If there are only few values, that variable can has.

>>> class SimpleConfig(ConfigBase):
...     @myproperty(options=[1, 2, 3])
...     def var(self) -> int:
...         2  # This means that value will not be set on init
...
>>> config = SimpleConfig()
>>> config.var = 4
Traceback (most recent call last):
KeyError: ...

You can also edit getter or setter. You can use lambda function (if more logic,
it's better to use normal property and add type checking manually).

Use setattr and name with underscore as prefix or self.private_name self means property, not config object.

>>> class SimpleConfig(ConfigBase):
...     @myproperty(
...         int,
...         fset=lambda self, object, new: (
...             print("I'm listener, i can call any function on change."),
...             setattr(object, self.private_name, new + 1),
...         ),
...     )
...     def with_setter() -> int:
...         return 1
...
>>> config = SimpleConfig()
>>> config.with_setter
1
>>> config.with_setter = 665
I'm listener, i can call any function on change.
>>> config.with_setter
666

Hierarchical config

>>> class Config(ConfigStructured):
...     def __init__(self) -> None:
...         self.subconfig1 = self.SubConfiguration1()
...         self.subconfig2 = self.SubConfiguration2()
...
...     class SubConfiguration1(ConfigBase):
...         @myproperty(options=[0, 1, 2, 3])
...         def value1() -> int:
...             '''Documentation here
...
...             Options: [0, 1, 2, 3]
...             '''
...             return 3
...
...         @myproperty
...         def value2(self):
...             return self.value1 + 1
...
...     class SubConfiguration2(ConfigBase):
...         @myproperty
...         def other_val(self):
...             return self.value2 + 1
...
>>> config = Config()
...
>>> config.subconfig2.other_val
5

You can access value from config as well as from subcategory

>>> config.other_val
5

This is how help looks like in VS Code

.. image:: /_static/options.png
    :width: 620
    :alt: tasks
    :align: center
"""

from typing import Any
import mylogging
import types as types_lib
import inspect

from .misc import validate


class MyProperty(property):
    def __init__(self, init_function, fget=None, fset=None, types=None, options=None, doc=None):
        self.init_function = init_function
        self.fget_new = fget if fget else self.default_fget
        self.fset_new = fset if fset else self.default_fset
        self.__doc__ = doc
        self.types = types
        self.options = options

    def default_fget(self, object):
        return getattr(object, self.private_name)

    def default_fset(self, object, content):
        setattr(object, self.private_name, content)

    def __set_name__(self, _, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, object, objtype=None):
        # If getting MyProperty class, not object, return MyProperty itself
        if not object:
            return self

        # Expected value can be nominal value or function, that return that value
        content = self.fget_new(object)
        if callable(content):
            if not len(content.__code__.co_varnames):
                value = content()
            else:
                value = content(object)
        else:
            value = content

        return value

    def __set__(self, object, content):

        # You can setup value or function, that return that value
        if callable(content):
            result = content(object)
        else:
            result = content

        validate(result, self.types, self.options, self.public_name)

        # Method defined can be pass as static method
        try:
            self.fset_new(object, content)
        except TypeError:
            self.fset_new(self, object, content)


def myproperty(types=None, options=None, fget=None, fset=None):
    """Wrapper for MyProperty to be able to use decorator with as well without params.
    e.g. @myproperty as well as @myproperty(options=[1, 2, 3]). Also for correct type hints.

    You can find working examples in module docstrings.

    Args:
        types (type): For example int, str or list.
        options (list): List of possible options. If value is not in options, error will be raised.
        fget (function, optional): Method that will get content. If none, default will be used. Defaults to None.
        fset (function, optional): Method that will set content. If none, default will be used. Defaults to None.

    Returns:
        function: Return wrapper that return property

    Note:
        If you set class variable itself, not on an object, you will remove all property and replace
        it with just a value.

    """
    # It's different if plain @decorator and if arguments. If no arguments, there is one param - function.
    if isinstance(types, types_lib.FunctionType):
        function = types
        types = None
    else:
        function = None

    def decorator(f):
        return MyProperty(
            init_function=f,
            fget=fget,
            fset=fset,
            doc=f.__doc__,
            types=types,
            options=options,
        )

    return decorator if not function else decorator(function)


class ConfigBase:
    """Main config class. If need nested config, use ConfigStructured instead.
    You can find working examples in module docstrings."""

    frozen = False
    _base_config_map = {}

    def __init__(self, frozen=None) -> None:

        self.myproperties_list = []

        for i in vars(type(self)).values():

            if isinstance(i, MyProperty):
                self.myproperties_list.append(i.public_name)
                setattr(self, i.private_name, i.init_function)

        if frozen is None:
            self.frozen = True
        else:
            self.frozen = frozen

    def __setattr__(self, name: str, value: Any) -> None:
        if (
            not self.frozen
            or name == "frozen"
            or name in [*self.myproperties_list, *vars(self), *self._base_config_map.keys()]
        ):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                mylogging.return_str(
                    f"Object {str(self)}is frozen. New attributes cannot be set. Maybe you misspelled name. "
                    "If you really need to change the value, set attribute frozen to false."
                )
            )

    def update(self, dict):
        for i, j in dict.items():
            setattr(self, i, j)

    def get_dict(self):
        return {
            # Values from object and from class
            **{
                key: value
                for key, value in self.__dict__.items()
                if not key.startswith("__")
                and not callable(value)
                and not hasattr(value, "myproperties_list")
                and key not in ["myproperties_list", "frozen", "_base_config_map"]
            },
            # Values from myproperties
            **{key: getattr(self, key) for key in self.myproperties_list},
        }


class ConfigStructuredMeta(type):
    """Metaclass that will edit Config class. Main reason is for being able to define own __init__ but
    still has some functionality from parent __init__. With this meta, there is no need to use super().

    As user, you probably will not need it. It's used internaly if inheriting from ConfigStructured."""

    def __init__(cls, name, bases, dct):
        def add_parent__init__(self, frozen=None, *a, **kw):

            self._base_config_map = {}

            cls.original__init__(self, *a, **kw)

            self.myproperties_list = []

            for i in vars(type(self)).values():

                if isinstance(i, MyProperty):
                    self.myproperties_list.append(i.public_name)
                    setattr(self, i.private_name, i.init_function)

            for i in vars(self).values():
                if hasattr(i, "myproperties_list"):
                    for j in i.myproperties_list:
                        self._base_config_map[j] = i
                    frozen = i.frozen
                    i.frozen = False
                    type(i).__getattr__ = self.__getattr__
                    i._base_config_map = self._base_config_map
                    i.frozen = frozen

            if frozen is None:
                self.frozen = True
            else:
                self.frozen = frozen

        cls.original__init__ = cls.__init__
        cls.__init__ = add_parent__init__


class ConfigStructured(ConfigBase, metaclass=ConfigStructuredMeta):
    """Class for creating config. Read why and how in config module docstrings."""

    def __getattr__(self, name: str):
        if name not in self._base_config_map:
            raise KeyError(mylogging.return_str(f"Variable {name} not found in config."))

        return getattr(self._base_config_map[name], name)

    def get_dict(self):
        # From main class
        dict_of_values = super().get_dict()
        # From sub configs
        for i in vars(self).values():
            if hasattr(i, "myproperties_list"):
                dict_of_values.update(i.get_dict())

        return dict_of_values
