# __init__.py for whit-phys-utils

name = "whit_phys_utils"
from ._version import __version__

VERSION = __version__.split(".")

from .git_access import *
from .pretty_fit import fitTable, prettyPolyFit
from .create_pdf import notebook_to_pdf

__all__ = ["local_repository", "fitTable", "prettyPolyFit", "notebook_to_pdf"]