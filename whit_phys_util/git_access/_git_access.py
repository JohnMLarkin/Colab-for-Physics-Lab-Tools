import os
import sys
from getpass import getpass

from ._run_cmd import run_secret_cmd, run_cmd
from ._git_settings import git_settings

# Based on code developed by Jordan Lueck and Paddy Alton
# https://pypi.org/project/colab-repoclone/

class LocalRepo:
    def __init__(self, repo, clone=True, branch="main", auth_method="env", expert_mode=False, verbose=False):
        """
        __init__

        Gathers user's GitHub credentials and either clones or initializes
        desired repository.

        """

        if auth_method == "env":
            self.env_authentication()
        else:
            self.cli_authentication()

        repo_url = repo.split("//")[1]
        if clone:
            self.repo_dir = repo.split("/")[-1].replace(".git", "")
        else:
            self.repo_dir = input("Local Repository :: ")

        self.access_repo = f"https://{self.github_user}:{self.github_token}@{repo_url}"
        self.branch = branch
        self.expert_mode = expert_mode

        run_cmd(f"git config --global user.name {self.github_user}")
        run_cmd(f"git config --global user.email {self.github_email}")
        run_cmd("git config --global init.defaultBranch main")

        self.in_colab = "google.colab" in sys.modules
        if self.in_colab:
            self.base_dir = '/content'
        else:
            self.base_dir = os.getcwd()
        self.repo_path = os.path.join(self.base_dir, self.repo_dir)

        if clone:
            self.clone(verbose)
        else:
            self.new()

    def clone(self, verbose=False):
        """
        clone

        Clones repository using username and access key.
        Set verbose=True to get output from clone command.
        """
        os.chdir(self.base_dir)
        if self.branch == "main":
            clone_cmd = f"git clone --progress {self.access_repo}"
        else:
            clone_cmd = f"git clone --progress --branch {self.branch} {self.access_repo}"
        run_secret_cmd(clone_cmd, verbose=verbose)
        os.chdir(self.repo_path)


    def new(self):
        """
        new

        Initializes a new repository in Google Colab environment using username and
        access key.

        """
        try:
            os.chdir(self.repo_path)
        except OSError:
            print(
                f"No directory named {self.repo_dir} exists. Are you sure you made it?"
            )
            return

        run_cmd("git init")
        origin = run_secret_cmd(f"git remote add origin {self.access_repo}", verbose=verbose)
        if origin:
            run_cmd("git remote rm origin")
            origin = run_secret_cmd(f"git remote add origin {self.access_repo}")
            if origin:
                print(
                    f"Command: < git remote add origin {self.access_repo} > failed. Check your permissions and that this repository exists on GitHub."
                )
                return


        ## First must pull (in case repo already exists), then push and set remote as upstream
        pull = run_cmd("git pull origin main --allow-unrelated-histories")
        if pull:
            print(
                "Command: < git pull origin main --allow-unrelated-histories > failed. Check your permissions."
            )
            return

        add = run_cmd("git add .")
        if add:
            print("Command: < git add . > failed. Check your permissions.")
            return

        commit = run_cmd("git commit -m 'First Commit from Google Colab'")
        if commit:
            print(
                f"Command: < git commit -m 'First Commit from Google Colab' > failed. Possibly because there were no files in /{self.repo_dir}"
            )
            return

        push = run_cmd("git push --set-upstream origin main")
        if push:
            print(
                "Command: < git push --set-upstream origin main > failed. Check your permissions."
            )


    def pull(self, verbose=False):
        """
        pull

        Pulls latest changes from GitHub repo into local Google Colab environment

        INPUTS:
            verbose=False - should output of git pull be displayed?

        """
        os.chdir(self.repo_path)
        pull = run_cmd("git pull", verbose=verbose)
        if pull:
            print("Command: < git pull > failed. Check your permissions.")

    def push(self, commit_msg=None, file_path=".", verbose=False):
        """
        push

        Commits and pushes latest changes to GitHub from Google Colab.

        KEYWORDS:
            commit_msg=None - message for this commit to GitHub. If none passed,
                will prompt for user input.
            file_path - path to specific files desired to push, defaults to all 
                files in repository.
            verbose=False - should output of git push be displayed?

        """
        if commit_msg is None:
            commit_msg = input("Commit Message :: ")

        check = """
        *************************************************************
        * Are you sure you want to push your changes?               *
        *                                                           *
        * Press "q" to abort. Press any other key to continue...    *
        *************************************************************
        """
        if input(check).lower() == "q":
            print("\n!! PUSH ABORTED !!\n")
            return

        os.chdir(self.repo_path)

        add = run_cmd(f"git add {file_path}")
        if add:
            print(f"Command: < git add {file_path} > failed. Check your permissions.")
            return

        commit = run_cmd(f"git commit -m '{commit_msg}'")
        if commit:
            print(
                f"Command: < git commit -m '{commit_msg}' > failed. Possibly because no changes were made. Also ensure there were no single or double quotation marks in your commit message."
            )
            return

        push = run_cmd("git push", verbose=verbose)
        if push:
            print("Command: < git push > failed. Check your permissions.")


    def new_branch(self, branch_name=None):
        """
        new_branch

        Creates a new branch off the current one and checks it out so future
        changes will be pushed to this new branch

        KEYWORDS:
            branch_name=None - the name of the new branch to create. If none
                passed, will prompt for user input.

        """
        if branch_name is None:
            branch_name = input("New Branch :: ")

        os.chdir(self.repo_path)

        brc = run_cmd(f"git branch {branch_name}")
        if brc:
            print(
                f"Command: < git branch {branch_name} > failed. Check your permissions."
            )
            return

        chk = run_cmd(f"git checkout {branch_name}")
        if chk:
            print(
                f"Command: < git checkout {branch_name} > failed. Check that this branch exists."
            )
            return

        self.branch = branch_name

        # Must push new branch to GitHub before making any changes to set the
        # upstream for future pushes from this branch
        push = run_cmd(f"git push --set-upstream origin {branch_name}")
        if push:
            print(
                f"Command: < git push --set-upstream origin {branch_name} > failed. Check your permissions."
            )


    def checkout(self, branch_name=None):
        """
        checkout

        Checks out an existing branch of the repository. All future pushes
        will push to this branch.

        KEYWORDS:
            branch_name=None - the name of the existing branch to checkout.
                If none passed, will prompt for user input.

        """

        if branch_name is None:
            branch_name = input("Checkout Branch :: ")

        os.chdir(self.repo_path)

        chk = run_cmd(f"git checkout {branch_name}")
        if chk:
            print(
                f"Command: < git checkout {branch_name} > failed. Check that this branch exists."
            )
            return

        self.branch = branch_name

    def reset(self, commit=None):
        """
        reset

        Performs a hard reset of the local repo to the specified commit,
        then force pushes this to rollback the repository, deleting all
        intermediate commits in the process.

        KEYWORDS:
            commit=None - the commit id to rollback to. If none passed,
                defaults to the previous commit.

        """
        check = """
        *****************************************************************
        *                         !! CAUTION !!                         *
        *                                                               *
        * Are you sure you want to rollback to a previous commit?       *
        *                                                               *
        * This is a hard reset, meaning all commits between the current *
        * and the one you are rolling back to will be lost.             *
        *                                                               *
        * Press "q" to abort. Press any other key to continue...        *
        *****************************************************************
        """
        if (not self.expert_mode):
            print("\n Repo reset is only permitted in expert mode \n")
            return

        if input(check).lower() == "q":
            print("\n!! RESET ABORTED !!\n")
            return

        os.chdir(self.repo_path)

        if commit is None:
            reset_cmd = "git reset --hard"
        else:
            reset_cmd = f"git reset --hard {commit}"

        reset = run_cmd(reset_cmd)
        if reset:
            print(
                f"Command: < {reset_cmd} > failed. Check the supplied commit id is a valid one."
            )

        push = run_cmd("git push --force")
        if push:
            print(f"Command: < git push --force > failed. Check your permissions.")


    def env_authentication(self):
        """
        env_authentication

        Checks for .env or .dotenv file with GitHub credentials. Used only when
        auth_method keyword passed to class instance is "env"

        """
        gs = git_settings()
        self.github_token = gs.gh_token
        self.github_user = gs.user_name
        self.github_email = gs.user_email
        if None in [self.github_token, self.github_user, self.github_email]:
            raise EnvironmentError(
                "Using auth_method='env', user_name, user_email, and gh_token must be \
                provided in .env or dotenv file"
            )

    def cli_authentication(self):
        """
        cli_authentication

        Uses getpass module to get user's GitHub credentials from standard input.
        Used only if auth_method keyword passed to class instance is *not* "env"

        """

        self.github_user = input("GitHub Username :: ")
        self.github_email = input("GitHub Email :: ")
        self.github_token = getpass("GitHub Authorization Token :: ")

