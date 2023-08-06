# This prevents a 'very funny' bug... without this line, joblib.Parallel throws an exception saying it cannot pickle
# PyCapsule object at FXEngine.run. No idea why it's working when importing joblib
# here (or at least before importing FXEngine)
import joblib

from ._version import __version__ as version_str

from trapeza import exception
from trapeza import metric
from trapeza import utils


__version__ = version_str
