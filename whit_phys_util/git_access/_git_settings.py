"""Load git environment settings

Looks for .env or dotenv file. If in Google Colab, tries to mount Google Drive
and look for the .env/dotenv file in /content/drive/MyDrive.
"""
# Approach inspired by the work of GitHub user ffreemt
# found at https://github.com/ffreemt/colab-misc-utils
import sys
from pydantic_settings import BaseSettings
from pathlib import Path

class git_settings(BaseSettings):
    user_name: str = ""
    user_email: str = ""
    gh_token: str = ""

    class Config:
        env_file = None # default setting
        if "google.colab" in sys.modules:
            basedir = Path("/content/drive/MyDrive")
            # if Google Drive is not mounted, do that now
            if not basedir.is_dir():
                from google.colab import drive
                drive.mount('/content/drive')
        else:
            basedir = Path.home()
        if basedir.joinpath(".env").is_file():
            env_file = basedir.joinpath(".env")
        elif basedir.joinpath("dotenv").is_file():
            env_file = basedir.joinpath("dotenv")
        elif basedir.joinpath("dotenv.txt").is_file():
            env_file = basedir.joinpath("dotenv.txt")



