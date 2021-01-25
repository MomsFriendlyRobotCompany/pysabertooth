
from .PySabertooth import Sabertooth

try:
    from importlib.metadata import version # type: ignore
except ImportError:
    from importlib_metadata import version # type: ignore

__author__ = 'Kevin J. Walchko'
__license__ = 'MIT'
__version__ = version("pysabertooth")
