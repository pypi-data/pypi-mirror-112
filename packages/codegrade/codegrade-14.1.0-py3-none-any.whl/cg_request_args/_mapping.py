"""This module contains parsers for various kinds of mappings.
"""
import abc
import copy
import enum
import uuid
import typing as t
import inspect
import datetime
import collections

from typing_extensions import Final, Literal, TypedDict

import cg_maybe
from cg_dt_utils import DatetimeWithTimezone

from ._base import Parser, SimpleValue
from ._enum import EnumValue, StringEnum
from ._list import List, TwoTuple
from ._query import QueryParam
from ._utils import USE_SLOTS as _USE_SLOTS
from ._utils import T as _T
from ._utils import is_typeddict
from ._nullable import Nullable
from ._any_value import AnyValue
from .exceptions import ParseError, SimpleParseError, MultipleParseErrors
from ._rich_value import RichValue
from ._swagger_utils import OpenAPISchema

__all__ = (
    'RequiredArgument',
    'OptionalArgument',
    'DefaultArgument',
    'OnExtraAction',
    'BaseFixedMapping',
    'FixedMapping',
    'LookupMapping',
)


class _BaseDict(TypedDict):
    pass


_Key = t.TypeVar('_Key', bound=str)
_BaseDictT = t.TypeVar('_BaseDictT', bound=_BaseDict)


class _Argument(t.Generic[_T, _Key]):
    if _USE_SLOTS:
        __slots__ = ('key', 'value', 'doc')

    def __init__(
        self,
        key: _Key,
        value: Parser[_T],
        doc: str,
    ) -> None:
        self.key: Final = key
        self.value: Final = value
        self.doc: Final = doc

    @abc.abstractmethod
    def describe(self) -> str:
        """Describe this argument.
        """
        ...

    @abc.abstractmethod
    def try_parse(self, value: t.Mapping[str, object]) -> t.Any:
        """Parse this argument.
        """
        ...

    def to_open_api(self, schema: OpenAPISchema) -> t.Mapping[str, t.Any]:
        """Convert this argument to open api.
        """
        # We save a copy in the common case here, as never call this method
        # when running the server, and adding a description copies the parser.
        return self.value.add_description(self.doc).to_open_api(schema)

    def _try_parse(self, value: t.Mapping[str, object]) -> cg_maybe.Maybe[_T]:
        if self.key not in value:
            return cg_maybe.Nothing

        found = value[self.key]
        try:
            return cg_maybe.Just(self.value.try_parse(found))
        except ParseError as err:
            raise err.add_location(self.key) from err


class RequiredArgument(t.Generic[_T, _Key], _Argument[_T, _Key]):
    """An argument in a ``FixedMapping`` that is required to be present.
    """

    def describe(self) -> str:
        return f'{self.key}: {self.value.describe()}'

    def try_parse(self, value: t.Mapping[str, object]) -> _T:
        """Try to parse this required argument from the given mapping.
        """
        res = self._try_parse(value)
        if isinstance(res, cg_maybe.Just):
            return res.value
        raise SimpleParseError(self.value,
                               cg_maybe.Nothing).add_location(self.key)


class DefaultArgument(t.Generic[_T, _Key], _Argument[_T, _Key]):
    """An argument in a ``FixedMapping`` that doesn't have to be present.
    """
    if _USE_SLOTS:
        __slots__ = ('__default', )

    def __init__(
        self,
        key: _Key,
        value: Parser[_T],
        doc: str,
        *,
        default: t.Callable[[], _T],
    ) -> None:
        super().__init__(key, value, doc)
        self.__default: Final = default

    def describe(self) -> str:
        return f'{self.key}?: {self.value.describe()}'

    def try_parse(self, value: t.Mapping[str, object]) -> _T:
        """Try to parse this required argument from the given mapping.
        """
        return self._try_parse(value).or_default_lazy(self.__default)

    def to_open_api(self, schema: OpenAPISchema) -> t.Mapping[str, t.Any]:
        """Convert this argument to open api.
        """
        return {
            **super().to_open_api(schema),
            'default': self.__default(),
        }


class OptionalArgument(t.Generic[_T, _Key], _Argument[_T, _Key]):
    """An argument in a ``FixedMapping`` that doesn't have to be present.
    """

    def describe(self) -> str:
        return f'{self.key}?: {self.value.describe()}'

    def try_parse(self, value: t.Mapping[str, object]) -> cg_maybe.Maybe[_T]:
        return self._try_parse(value)


class _DictGetter(t.Generic[_BaseDictT]):
    if _USE_SLOTS:
        __slots__ = ('__data', )

    def __init__(self, data: _BaseDictT) -> None:
        self.__data = data

    if not t.TYPE_CHECKING:

        def _unsafe_get_base_data(self) -> t.Dict[str, t.Any]:
            return copy.copy(self.__data)

    def __repr__(self) -> str:
        return '_DictGetter({!r})'.format(self.__data)

    def __getattr__(self, key: str) -> object:
        try:
            return self.__data[key]
        except KeyError:
            return super().__getattribute__(key)


_BaseFixedMappingT = t.TypeVar('_BaseFixedMappingT', bound='_BaseFixedMapping')


class OnExtraAction(enum.Enum):
    """Action to perform if a :class:`_BaseFixedMapping` finds keys in the
    dictionary it is parsing that were not defined on the parser.
    """
    nothing = enum.auto()
    warning = enum.auto()
    error = enum.auto()


class _BaseFixedMapping(t.Generic[_BaseDictT]):
    def __init__(self, arguments: t.Sequence[_Argument]) -> None:
        super().__init__()
        self._arguments = arguments
        self.__schema: t.Optional[t.Type[_BaseDictT]] = None
        self._on_extra = OnExtraAction.nothing

    def set_on_extra(
        self: _BaseFixedMappingT, value: OnExtraAction
    ) -> _BaseFixedMappingT:
        """Enable warnings or errors when extra keys are found in the
        dictionaries to parse.
        """
        res = copy.copy(self)
        res._on_extra = value  # pylint: disable=protected-access
        return res

    @abc.abstractmethod
    def describe(self) -> str:
        """Describe this parser.
        """
        raise NotImplementedError

    def _describe(self, readable: bool) -> str:
        if readable and len(list(self._arguments)) > 1:
            import textwrap  # pylint: disable=import-outside-toplevel

            args = [
                arg.describe()
                for arg in sorted(self._arguments, key=lambda a: a.key)
            ]
            indent = ' ' * 4
            content = '\n{},\n'.format(
                ',\n'.join(textwrap.indent(arg, indent) for arg in args)
            )
        else:
            args = [arg.describe() for arg in self._arguments]
            content = ', '.join(args)
        return 'Mapping[{}]'.format(content)

    def to_open_api_as_query(self, schema: OpenAPISchema
                             ) -> t.Sequence[t.Mapping[str, t.Any]]:
        """Convert this mapping to a OpenAPI object as if it were used as a
        query string.
        """
        return [{
            'in': 'query',
            'name': arg.key,
            'schema': arg.to_open_api(schema),
            'description': schema.make_comment(arg.doc),
            'required': isinstance(arg, RequiredArgument),
        } for arg in self._arguments]

    def _to_open_api(self, schema: OpenAPISchema) -> t.Mapping[str, t.Any]:
        required = [
            arg.key for arg in self._arguments
            if isinstance(arg, RequiredArgument)
        ]
        res = {
            'type': 'object',
            'properties': {
                arg.key: arg.to_open_api(schema)
                for arg in self._arguments
            },
        }
        if required:
            res['required'] = required
        return res

    def _try_parse(
        self,
        value: object,
    ) -> _BaseDictT:
        if not isinstance(value, dict):
            raise SimpleParseError(self, value)

        result = {}
        errors = []
        for arg in self._arguments:
            try:
                result[arg.key] = arg.try_parse(value)
            except ParseError as exc:
                errors.append(exc)

        if errors:
            raise MultipleParseErrors(self, value, errors)

        extra_keys = value.keys() - result.keys()
        if extra_keys:
            if self._on_extra is OnExtraAction.warning:
                import warnings  # pylint: disable=import-outside-toplevel
                warnings.warn(
                    'Got extra keys: {}'.format(extra_keys),
                    stacklevel=3,
                )
            elif self._on_extra is OnExtraAction.error:
                extra_keys_str = ', '.join(extra_keys)
                raise SimpleParseError(
                    self,
                    value,
                    extra={
                        'extra_keys': extra_keys_str,
                        'message': f'Got extra keys: {extra_keys_str}',
                    }
                )

        return t.cast(_BaseDictT, result)


class BaseFixedMapping(
    t.Generic[_BaseDictT], _BaseFixedMapping[_BaseDictT], Parser[_BaseDictT]
):
    """A fixed mapping that returns a dictionary instead of a ``_DictGetter``.

    .. note::

        You should only create this using
        :meth:`.BaseFixedMapping.from_typeddict`, not using the normal
        constructor.
    """

    def __init__(
        self,
        *arguments: object,
        schema: t.Optional[t.Type[_BaseDictT]],
    ) -> None:
        super().__init__(t.cast(t.Any, arguments))
        self.__has_optional = any(
            isinstance(arg, OptionalArgument) for arg in self._arguments
        )
        self.__schema: t.Optional[t.Type[_BaseDictT]] = schema

    def _to_open_api(self, schema: OpenAPISchema) -> t.Mapping[str, t.Any]:
        if self.__schema is None:
            return super()._to_open_api(schema)
        else:
            return schema.add_schema(self.__schema)

    def describe(self) -> str:
        return self._describe(self._use_readable_describe)

    def try_parse(self, value: object) -> _BaseDictT:
        res = self._try_parse(value)
        # Optional values are parsed as Maybe, but callers think they will
        # simply get a dict with possibly missing items. So we convert that
        # here.
        if not self.__has_optional:
            return res

        for arg in self._arguments:
            if not isinstance(arg, OptionalArgument):
                continue

            key = arg.key
            if cg_maybe.Nothing.is_nothing_instance(res[key]):
                del res[key]
            else:
                assert isinstance(res[key], cg_maybe.Just)
                res[key] = res[key].value  # type: ignore

        return res

    @classmethod
    def __from_python_type(cls, typ, from_query):  # type: ignore
        # pylint: disable=too-many-return-statements,too-many-nested-blocks,too-many-branches
        # This function doesn't play nice at all with our plugins, so simply
        # skip checking it.
        origin = getattr(typ, '__origin__', None)

        def assert_not_query(cond: bool = False) -> None:
            if from_query and not cond:  # pragma: no cover
                raise AssertionError(
                    '{} is not supported as query param'.format(typ)
                )

        if is_typeddict(typ):
            args = []
            for key, subtyp in typ.__annotations__.items():
                if key in typ.__required_keys__:
                    args.append(
                        RequiredArgument(
                            key,
                            cls.__from_python_type(subtyp, from_query),
                            '',
                        )
                    )
                else:
                    args.append(
                        OptionalArgument(
                            key,
                            cls.__from_python_type(subtyp, from_query),
                            '',
                        )
                    )
            return BaseFixedMapping(*args, schema=typ)
        elif typ in (str, int, bool, float):
            if from_query:
                return getattr(QueryParam, typ.__name__)
            else:
                return getattr(SimpleValue, typ.__name__)
        elif origin in (list, collections.abc.Sequence):
            assert_not_query()

            return List(cls.__from_python_type(typ.__args__[0], from_query))
        elif origin == t.Union:
            has_none = type(None) in typ.__args__
            assert_not_query(not has_none)

            first_arg, *args = [a for a in typ.__args__ if a != type(None)]
            res = cls.__from_python_type(first_arg, from_query)
            for item in args:
                res = res | cls.__from_python_type(item, from_query)
            return Nullable(res) if has_none else res
        elif origin == Literal:
            assert all(isinstance(arg, str) for arg in typ.__args__)
            return StringEnum(*typ.__args__)
        elif isinstance(typ, enum.EnumMeta):
            return EnumValue(typ)
        elif origin == dict:
            assert_not_query()

            key, value = typ.__args__
            assert key == str, (
                'Only mappings with strings as keys are supported'
            )
            return LookupMapping(cls.__from_python_type(value, from_query))
        elif typ == uuid.UUID:
            return RichValue.UUID
        elif origin == tuple and len(typ.__args__) == 2:
            assert_not_query()

            return TwoTuple(
                cls.__from_python_type(typ.__args__[0], from_query),
                cls.__from_python_type(typ.__args__[1], from_query),
            )
        elif typ == DatetimeWithTimezone:
            return RichValue.DateTime
        elif typ == datetime.timedelta:
            assert_not_query()
            return RichValue.TimeDelta
        elif typ == t.Any:
            return AnyValue
        else:  # pragma: no cover
            raise AssertionError(
                f'Could not convert: {typ} (origin: {origin})'
            )

    @classmethod
    def from_function_parameters_list(
        cls,
        params: t.Iterable[inspect.Parameter],
        from_query: bool,
    ) -> 'BaseFixedMapping[t.Any]':
        """Create a BaseFixedMapping from a list of function parameters.
        """
        args = []
        for param in params:
            if param.default == inspect.Parameter.empty:
                args.append(
                    RequiredArgument(  # type: ignore
                        param.name,
                        cls.__from_python_type(param.annotation, from_query),
                        '',
                    )
                )
            else:
                default = param.default

                args.append(
                    DefaultArgument(  # type: ignore
                        param.name,
                        cls.__from_python_type(param.annotation, from_query),
                        '',
                        default=t.cast(
                            t.Callable,
                            lambda _default=default: _default,
                        ),
                    )
                )
        return BaseFixedMapping(  # type: ignore
            *args, schema=None
        )

    @classmethod
    def from_function(cls, fun: t.Callable) -> 'BaseFixedMapping[t.Any]':
        """Create a mapping from a function signature.
        """
        return cls.from_function_parameters_list(
            inspect.signature(fun).parameters.values(),
            from_query=False,
        )

    @classmethod
    def from_typeddict(cls, typeddict: t.Type) -> 'BaseFixedMapping[t.Any]':
        """Create a mapping from an existing typeddict.
        """
        return cls.__from_python_type(typeddict, False)


class FixedMapping(
    t.Generic[_BaseDictT], _BaseFixedMapping[_BaseDictT],
    Parser[_DictGetter[_BaseDictT]]
):
    """A mapping in which the keys are fixed and the values can have different
    types.
    """

    def __init__(self, *arguments: object) -> None:
        super().__init__(t.cast(t.Any, arguments))
        self.__tag: t.Optional[t.Tuple[str, object]] = None

    def describe(self) -> str:
        return self._describe(self._use_readable_describe)

    def add_tag(self, key: str, value: object) -> 'FixedMapping[_BaseDictT]':
        """Add a tag to this mapping.

        This tag will always be added to the final mapping after parsing.

        :param key: The key of the tag, should be a literal string.
        :param value: The value of the tag, should be a literal string.

        :returns: The existing mapping but mutated.
        """
        self.__tag = (key, value)
        return self

    def try_parse(
        self,
        value: object,
    ) -> _DictGetter[_BaseDictT]:
        result = self._try_parse(value)

        if self.__tag is not None:
            result[self.__tag[0]] = self.__tag[1]  # type: ignore[misc]
        return _DictGetter(result)

    def combine(
        self, other: 'FixedMapping[t.Any]'
    ) -> 'FixedMapping[_BaseDict]':
        """Combine this fixed mapping with another.

        :param other: The mapping to combine with. The arguments are not
            allowed to overlap

        :returns: A new fixed mapping with arguments of both given mappings.
        """
        args = [*self._arguments, *other._arguments]  # pylint: disable=protected-access
        return FixedMapping(*args)  # type: ignore


class LookupMapping(t.Generic[_T], Parser[t.Mapping[str, _T]]):
    """A parser that implements a lookup mapping.

    This a mapping where the keys are not fixed, so only the values are parsed
    (and are all parsed the same). Currently only string keys are allowed.
    """
    if _USE_SLOTS:
        __slots__ = ('__parser', )

    _PARSE_KEY = SimpleValue.str

    def __init__(self, parser: Parser[_T]) -> None:
        super().__init__()
        self.__parser = parser

    def describe(self) -> str:
        return 'Mapping[str: {}]'.format(self.__parser.describe())

    def _to_open_api(self, schema: OpenAPISchema) -> t.Mapping[str, t.Any]:
        return {
            'type': 'object',
            'additionalProperties': self.__parser.to_open_api(schema),
        }

    def try_parse(self, value: object) -> t.Mapping[str, _T]:
        if not isinstance(value, dict):
            raise SimpleParseError(self, value)

        result = {}
        errors = []
        for key, val in value.items():
            try:
                parsed_key = self._PARSE_KEY.try_parse(key)
                result[parsed_key] = self.__parser.try_parse(val)
            except ParseError as exc:
                errors.append(exc.add_location(str(key)))
        if errors:
            raise MultipleParseErrors(self, value, errors)

        return result
