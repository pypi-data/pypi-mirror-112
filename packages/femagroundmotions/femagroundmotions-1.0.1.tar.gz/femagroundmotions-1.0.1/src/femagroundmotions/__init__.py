import importlib.resources

__version__ = importlib.resources.read_text(__name__, '__version__')

from .atcparse import AtcParser
from .hdf5 import from_hdf5, to_hdf5
