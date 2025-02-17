from __future__ import annotations

from collections.abc import Callable
from contextlib import closing
from typing import Any, Protocol, TypeVar, overload

import attrs

from pyramid.config import Configurator
from pyramid.registry import Registry
from pyramid.request import Request
from pyramid.response import Response
from pyramid.threadlocal import get_current_registry, get_current_request

import svcs


def svcs_from(request: Request | None = None) -> svcs.Container:
    """
    Get the current container either from *request* or from thread locals.

    Arguments:

        request: If None, thread locals are used.
    """
    if request:
        return request.svcs  # type: ignore[no-any-return]

    return get_current_request().svcs  # type: ignore[no-any-return]


def init(
    config: Configurator,
    registry: svcs.Registry | None = None,
    *,
    tween_under: Any = None,
    tween_over: Any = None,
) -> None:
    """
    Configure *config* to work with *svcs*.

    *svcs* uses a :term:`tween` to manage the life cycle of the container. You
    can affect its position by passing *tween_under* and *tween_over*.

    .. _Tween: https://docs.pylonsproject.org/projects/pyramid/en/main/glossary.html#term-tween

    Args:
        config: Pyramid configurator object.

        registry: A custom *svcs* registry to use. If None, a new one is created.

        tween_under: Passed unchanged to
            :meth:`pyramid.config.Configurator.add_tween()` as *under*.

        tween_over: Passed unchanged to
            :meth:`pyramid.config.Configurator.add_tween()` as *over*.
    """
    config.registry[_KEY_REGISTRY] = registry or svcs.Registry()

    config.add_tween(
        "svcs.pyramid.ServicesTween", over=tween_over, under=tween_under
    )


_KEY_REGISTRY = "svcs_registry"


@attrs.define
class ServicesTween:
    """
    Handle *svcs* container life cycle for a Pyramid request.
    """

    handler: Callable[[Request], Response]
    registry: Registry

    def __call__(self, request: Request) -> Response:
        with closing(svcs.Container(self.registry[_KEY_REGISTRY])) as con:
            request.svcs = con

            return self.handler(request)


def register_factory(
    config: PyramidRegistryHaver,
    svc_type: type,
    factory: Callable,
    *,
    ping: Callable | None = None,
    on_registry_close: Callable | None = None,
) -> None:
    """
    Same as :meth:`svcs.Registry.register_factory()`, but uses registry on
    *config*.
    """
    config.registry[_KEY_REGISTRY].register_factory(
        svc_type, factory, ping=ping, on_registry_close=on_registry_close
    )


def register_value(
    config: PyramidRegistryHaver,
    svc_type: type,
    value: object,
    *,
    ping: Callable | None = None,
    on_registry_close: Callable | None = None,
) -> None:
    """
    Same as :meth:`svcs.Registry.register_value()`, but uses registry on
    *config*.
    """
    config.registry[_KEY_REGISTRY].register_value(
        svc_type, value, ping=ping, on_registry_close=on_registry_close
    )


def close_registry(rh: PyramidRegistryHaver) -> None:
    """
    Close the registry on *rh*, if present.

    Ideal for :func:`atexit.register()` handlers.

    Parameters:
        rh: An object that carries a :class:`pyramid.registry.Registry`.
    """
    if reg := rh.registry.pop(_KEY_REGISTRY, None):
        reg.close()


class PyramidRegistryHaver(Protocol):
    """
    An object with a :class:`pyramid.registry.Registry` as a ``registry``
    attribute. For example a :class:`~pyramid.config.Configurator` or an
    application.
    """

    registry: dict[str, Any]


def get_registry(rh: PyramidRegistryHaver | None = None) -> svcs.Registry:
    """
    Get the registry from *rh* or thread locals.

    Arguments:
        rh: If None, thread locals are used.
    """
    if rh:
        return rh.registry[_KEY_REGISTRY]  # type: ignore[no-any-return]

    return get_current_registry()[_KEY_REGISTRY]  # type: ignore[no-any-return]


def get_abstract(*svc_types: type) -> Any:
    """
    Same as :meth:`svcs.Container.get_abstract()`, but uses container on
    thread locals.
    """
    return get(*svc_types)


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")
T10 = TypeVar("T10")


@overload
def get(svc_type: type[T1], /) -> T1:
    ...


@overload
def get(svc_type1: type[T1], svc_type2: type[T2], /) -> tuple[T1, T2]:
    ...


@overload
def get(
    svc_type1: type[T1], svc_type2: type[T2], svc_type3: type[T3], /
) -> tuple[T1, T2, T3]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    /,
) -> tuple[T1, T2, T3, T4]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    svc_type5: type[T5],
    /,
) -> tuple[T1, T2, T3, T4, T5]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    svc_type5: type[T5],
    svc_type6: type[T6],
    /,
) -> tuple[T1, T2, T3, T4, T5, T6]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    svc_type5: type[T5],
    svc_type6: type[T6],
    svc_type7: type[T7],
    /,
) -> tuple[T1, T2, T3, T4, T5, T6, T7]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    svc_type5: type[T5],
    svc_type6: type[T6],
    svc_type7: type[T7],
    svc_type8: type[T8],
    /,
) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    svc_type5: type[T5],
    svc_type6: type[T6],
    svc_type7: type[T7],
    svc_type8: type[T8],
    svc_type9: type[T9],
    /,
) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8, T9]:
    ...


@overload
def get(
    svc_type1: type[T1],
    svc_type2: type[T2],
    svc_type3: type[T3],
    svc_type4: type[T4],
    svc_type5: type[T5],
    svc_type6: type[T6],
    svc_type7: type[T7],
    svc_type8: type[T8],
    svc_type9: type[T9],
    svc_type10: type[T10],
    /,
) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]:
    ...


def get(*svc_types: type) -> object:
    """
    Same as :meth:`svcs.Container.get()`, but uses thread locals to find the
    current request.
    """
    return svcs_from().get(*svc_types)
