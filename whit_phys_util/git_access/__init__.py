from ._git_access import LocalRepo

def local_repository(repo, clone=True, branch="main", auth_method="env", expert_mode=False, verbose=False):
    """
    local_repository

    Call this method to create an instance of a GitHub repository in the 
    Google Colab environment. You can then use the class methods to push
    and pull from this repo, among other things, directly from Colab.

    INPUTS:
        repo - the link to the GitHub repository for cloning or the empty
                GitHub repo for initializing

    KEYWORDS:
        clone=True - indicates whether a new repository is being created
            locally and uploaded to GitHub, rather than a clone
        branch="main" - the specific branch to clone, if desired
        auth_method="env" - indicates where to look for your GitHub credentials.
            "env" will expect them in a .env or dotenv file on Google Drive, anything
            else will prompt the user to input them.
        expert_mode=False - indicates whether higher risk git commands are permitted
        verbose=False - indicates whether output of selected git commands should be displayed

    RETURNS:
        A LocalRepo instance
    """
    # Branch is forced to "main" for creating new repositories
    if not clone:
        branch = "main"

    return LocalRepo(repo, clone=clone, branch=branch, auth_method=auth_method, expert_mode = expert_mode, verbose=False)

__all__ = ["local_repository"]
