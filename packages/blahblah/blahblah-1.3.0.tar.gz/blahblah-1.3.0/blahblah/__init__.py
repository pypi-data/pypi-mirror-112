from typing import Any

from district42 import GenericSchema
from district42.types import Schema

from ._generator import Generator
from ._random import Random
from ._regex_generator import RegexGenerator
from ._version import version

__version__ = version
__all__ = ("fake", "Generator", "Random", "RegexGenerator",)

_random = Random()
_generator = Generator(_random, RegexGenerator(_random))


def fake(schema: GenericSchema, **kwargs: Any) -> Any:
    return schema.__accept__(_generator, **kwargs)


Schema.__override__(Schema.__invert__.__name__, fake)
