# json-deserializer

Attempts to deserialize objects into a format that json.dumps/json.loads can use.
- Anything that is a Sequence, but not a str will be cast to a list.
- All Mappings will be cast to dicts
- Decimal to floats
- Callable to string (will return Object.__repr__)


## Usage Example

```python
    >>> from json import dumps
    >>> from collections import UserDict
    >>> from json_deserializer import deserialize
    >>>
    >>> class MyDict(UserDict):
    >>>     pass
    >>>
    >>> d = MyDict({"foo": "bar"})
    >>> try:
    >>>    dumps(d)
    >>> except Exception as e:
    >>>    print(e)
    Object of type MyDict is not JSON serializable
    >>> dumps(d, default=deserialize)
    '{"foo": "bar"}'
