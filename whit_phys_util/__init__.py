# __init__.py for whit-phys-utils

name = "whit_phys_utils"
__version__ = "0.1.6.dev7"
VERSION = __version__.split(".")

from .git_access import *
from .pretty_fit import fitTable, prettyPolyFit

__all__ = ["__version__","local_repository", "fitTable", "prettyPolyFit"]