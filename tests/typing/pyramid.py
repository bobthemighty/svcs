# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from typing import Generator

import pyramid

from pyramid.config import Configurator

import svcs


def factory_with_cleanup() -> Generator[int, None, None]:
    yield 1


config = Configurator(settings={})

svcs.pyramid.init(config)

svcs.pyramid.register_value(config, int, 1)
svcs.pyramid.register_value(config, int, 1, ping=lambda: None)

svcs.pyramid.register_factory(config, str, str)
svcs.pyramid.register_factory(config, int, factory_with_cleanup)
svcs.pyramid.register_value(config, str, str, ping=lambda: None)

o1: object = svcs.pyramid.get(object)
o2: int = svcs.pyramid.get_abstract(object)

a: int
b: str
c: bool
d: tuple
e: object
f: float
g: list
h: dict
i: set
j: bytes
a, b, c, d, e, f, g, h, i, j = svcs.pyramid.get(
    int, str, bool, tuple, object, float, list, dict, set, bytes
)

reg: svcs.Registry = svcs.pyramid.get_registry(config)
reg = svcs.pyramid.get_registry()

con: svcs.Container = svcs.pyramid.svcs_from()
con = svcs.pyramid.svcs_from(pyramid.request.Request())

svcs.pyramid.close_registry(config)
