# __init__.py for whit-phys-utils

name = "whit_phys_utils"
from ._version import __version__

VERSION = __version__.split(".")

from .pretty_fit import fitTable, prettyPolyFit
from .dynamic_data_entry import DynamicDataEntry

import sys
IN_COLAB = 'google.colab' in sys.modules
if IN_COLAB:
    from .git_access import *
    from .create_pdf import notebook_to_pdf
    __all__ = ["local_repository", "fitTable", "prettyPolyFit", "notebook_to_pdf","DynamicDataEntry"]
else:
    __all__ = ["fitTable", "prettyPolyFit"]