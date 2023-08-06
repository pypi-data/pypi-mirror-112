from decimal import Decimal
from typing import (
    Sequence,
    Mapping,
    Any,
    Callable
)


class Deserializer:
    """
    For objects that are `almost` a duck, but not quite
    This keeps json decoder from blowing up. Suitable for use
    as `default` keyword arg to json.dumps if `recursive` is set
    to False. An example of an almost duck is UserDict, which will
    behave like a dict in almost every way, but json.dumps doesn't know
    what to do with.
    """

    #: Will be called on anything that can't be resolved by our logic
    default: Callable = str

    #: If set then we will resolve through every bit of the data
    recursive: bool = False

    @classmethod
    def deserialize(
        cls,
        data: Any,
        recursive: bool = None,
        default: Callable = None
    ) -> Any:

        recursive = recursive if recursive is not None else cls.recursive
        default = default if default is not None else cls.default

        if isinstance(data, Mapping) and not isinstance(data, dict):
            if recursive:
                res = cls.deserialize(dict(data), recursive=recursive)
            else:
                res = dict(data)

        elif isinstance(data, Sequence) and not isinstance(data, str):
            if recursive:
                res = [
                    cls.deserialize(x, recursive=recursive) for x in data
                ]
            else:
                res = list(data)

        elif isinstance(data, dict):
            if recursive:
                res = {}
                for k, v in data.items():
                    res[k] = cls.deserialize(v, recursive=recursive)
            else:
                res = data

        elif isinstance(data, Callable):
            res = str(data)

        elif isinstance(data, Decimal):
            res = float(data)

        # Fall back to default of str
        elif default:
            res = default(data)

        # If recursive is set to True and we are running as the default decoder
        # for json.dumps then we will cause an error due to recursion by returning the
        # original response. But if we are running standalone then this is suitable so
        # that we don't return None for values that don't need to be decoded.
        elif recursive:
            res = data

        return res

    @classmethod
    def deserialize_recursive(
        cls,
        data: Any,
        default: Callable = None
    ) -> Any:
        return cls.deserialize(data, recursive=True, default=default)


def deserialize(
    data: Any,
    default: Callable = None,
    recursive: bool = False
):
    return Deserializer.deserialize(
        data=data,
        default=default,
        recursive=recursive
    )