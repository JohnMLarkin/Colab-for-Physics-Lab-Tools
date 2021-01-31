# __init__.py for whit-phys-utils

name = "whit_phys_utils"
with open("../version.txt", "r", encoding="utf-8") as fh:
    __version__ = fh.read()

VERSION = __version__.split(".")

from .git_access import *
from .pretty_fit import fitTable, prettyPolyFit

__all__ = ["__version__","local_repository", "fitTable", "prettyPolyFit"]