import numpy as np
import functools


def selfisparent(func):
    # replaces self with parent attribute, which should be the instance calling the subclass methods
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        out = func(args[0].parent, *args[1:], **kwargs)
        return out

    return wrapper


def inplace(method):
    # makes method behavior act in-place by default and allows an "inplace" boolean kwarg to turn off

    @functools.wraps(method)
    def wrapper(self, *args, inplace=True, **kwargs):
        if inplace and not self.flags.owndata:
            raise Exception(
                "NDArray is not the source of its data. Copy image before applying inplace operation:\n"
                + "instance.copy().*operation*"
            )

        out = method(self, *args, **kwargs)
        if type(out) == tuple:
            data, supplemental = [out[0], out[1:]]
        else:
            data = out
            supplemental = ()

        if not issubclass(type(data), np.ndarray):
            inplace = False
        if inplace:
            self.resize((0,), refcheck=False)
            self.dtype = data.dtype
            self.resize(data.shape, refcheck=False)
            self[:] = data
            if supplemental:
                return (self, *supplemental)
            else:
                return self
        else:
            if supplemental:
                return (data, *supplemental)
            else:
                return data

    return wrapper


def for_all_methods(*decorators):
    "Decorates all non-dunder methods of a class with a set of decorators"

    def decorate(cls):
        for attr in cls.__dict__:
            for decorator in decorators:
                if callable(getattr(cls, attr)) and "__" not in attr:
                    setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate
