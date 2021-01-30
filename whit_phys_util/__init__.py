# __init__.py for whit-phys-utils

name = "whit_phys_utils"
__version__ = "0.1.6.dev2"
VERSION = __version__.split(".")

from .git_access import *
from .pretty_fit import fitTable, prettyPolyFit

# def local_repository(repo, clone=True, branch="main", auth_method="env"):
#     """
#     local_repository

#     Call this method to create an instance of a GitHub repository in the 
#     Google Colab environment. You can then use the class methods to push
#     and pull from this repo, among other things, directly from Colab.

#     INPUTS:
#         repo - the link to the GitHub repository for cloning or the empty
#                 GitHub repo for initializing

#     KEYWORDS:
#         clone=True - indicates whether a new repository is being created
#             locally and uploaded to GitHub, rather than a clone
#         branch="main" - the specific branch to clone, if desired
#         auth_method="env" - indicates where to look for your GitHub credentials.
#             "env" will expect them in a .env or dotenv file on Google Drive, anything
#             else will prompt the user to input them.

#     RETURNS:
#         A LocalRepo instance
#     """
#     # Branch is forced to "main" for creating new repositories
#     if not clone:
#         branch = "main"

#     return LocalRepo(repo, clone=clone, branch=branch, auth_method=auth_method)

__all__ = ["local_repository", "fitTable", "prettyPolyFit"]