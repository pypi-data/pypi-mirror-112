import pkg_resources

from .core import engine
from .decorators import flow

__all__ = (
    "engine",
    "flow",
)

__version__ = pkg_resources.get_distribution(__package__).version
